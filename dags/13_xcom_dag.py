from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


dag = DAG(
    "xcom_dag",
    description="Group Task Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

def task_write(**kwarg):
    kwarg['ti'].xcom_push(key='valor_xcom1', value=10200)

def task_read(**kwarg):
    value = kwarg['ti'].xcom_pull(key='valor_xcom1')
    print(f"Value retrivied: {value}")

task_write = PythonOperator(task_id="task_write", python_callable=task_write, dag=dag)
task_read = PythonOperator(task_id="task_read", python_callable=task_read, dag=dag)

task_write >> task_read