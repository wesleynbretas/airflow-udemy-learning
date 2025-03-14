from pickle import FALSE
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import json
import os

default_args = {
    'depends_on_past' : False,
    'email' : ['wesley.bretas@outlook.com'],
    'email_on_failure' : True,
    'email_on_retry' : False,
    'retries': 1,
    'retry_delay' : timedelta(seconds=20)
}

dag = DAG(
    "wind_turbine_dag",
    description="Wind Turbine DAG",
    schedule_interval=None,
    default_args=default_args,
    start_date=datetime(2025, 3, 12),
    catchup=False,
    default_view="graph",
    doc_md="Wind Turbine Data"
)

check_temperature_group = TaskGroup("check_temperature_group", dag=dag)
database_group = TaskGroup("database_group", dag=dag)

file_sensor_task = FileSensor(
    task_id = "file_sensor_task",
    filepath = Variable.get("windturbine_file_path"),
    fs_conn_id = "fs-windturbine-data",
    poke_interval = 10,
    dag = dag
)

def process_file(**kwarg):
    with open(Variable.get("windturbine_file_path")) as f:
        data = json.load(f)
        kwarg["ti"].xcom_push(key="idtemp", value=data["idtemp"])
        kwarg["ti"].xcom_push(key="powerfactor", value=data["powerfactor"])
        kwarg["ti"].xcom_push(key="hydraulicpressure", value=data["hydraulicpressure"])
        kwarg["ti"].xcom_push(key="temperature", value=data["temperature"])
        kwarg["ti"].xcom_push(key="timestamp", value=data["timestamp"])

    os.remove(Variable.get("windturbine_file_path"))

get_data_task = PythonOperator(
    task_id = "get_data_task",
    python_callable = process_file,
    provide_context = True,
    dag = dag

)

def create_table():
    create_query = """
        CREATE TABLE IF NOT EXISTS sensors (idtemp varchar, powerfactor varchar, hydraulicpressure varchar, temperature varchar, timestamp varchar)
    """

    pg_hook = PostgresHook(postgres_conn_id="postgres-postgres")
    pg_hook.run(create_query, autocommit=True)

create_table_task = PythonOperator(
    task_id="create_table_task",
    python_callable=create_table,
    task_group=database_group,
    dag=dag
)

def insert_data(**kwargs):
    parameters=(
        '{{ ti.xcom_pull(task_ids="get_data_task",key="idtemp") }}',     
        '{{ ti.xcom_pull(task_ids="get_data_task",key="powerfactor") }}',     
        '{{ ti.xcom_pull(task_ids="get_data_task",key="hydraulicpressure") }}',     
        '{{ ti.xcom_pull(task_ids="get_data_task",key="temperature") }}',     
        '{{ ti.xcom_pull(task_ids="get_data_task",key="timestamp") }}'                                                                               
    )

    insert_query = """
        INSERT INTO sensors (idtemp, powerfactor, hydraulicpressure, temperature, timestamp) 
        VALUES (%s, %s, %s, %s, %s);
    """

    pg_hook = PostgresHook(postgres_conn_id="postgres-postgres")
    pg_hook.run(insert_query, parameters=parameters, autocommit=True)

insert_data_task = PythonOperator(
    task_id="insert_data_task",
    python_callable=insert_data,
    task_group=database_group,
    dag=dag
)

send_email_alert_task = EmailOperator(
    task_id="send_email_alert_task",
    to = "wesley.bretas@outlook.com",
    subject = "Airflow Alert",
    html_content = '''<h3>Alerta de Temperatrura. </h3>
        <p> Dag: windturbine </p>
    ''',
    task_group = check_temperature_group,
    dag=dag
)

send_email_normal_task = EmailOperator(
    task_id="send_email_normal_task",
    to = "wesley.bretas@outlook.com",
    subject = "Airflow Advise",
    html_content = '''<h3>Temperatrura normais. </h3>
        <p> Dag: windturbine </p>
    ''',
    task_group = check_temperature_group,
    dag=dag
)

def check_temperature(**context):
    number = float(context['ti'].xcom_pull(task_ids="get_data_task", key="temperature"))
    
    if number >= 24:
        return "check_temperature_group.send_email_alert_task"
    else:
        return "check_temperature_group.send_email_normal_task"

check_temperature_branch_task = BranchPythonOperator(
    task_id="check_temperature_branch_task",
    python_callable=check_temperature,
    provide_context =True,
    task_group=check_temperature_group,
    dag=dag
)

with check_temperature_group:
    check_temperature_branch_task >> [send_email_alert_task, send_email_normal_task]

with database_group:
    create_table_task >> insert_data_task

file_sensor_task >> get_data_task
get_data_task >> check_temperature_group
get_data_task >> database_group