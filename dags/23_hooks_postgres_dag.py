from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook

dag = DAG(
    "hooks",
    description="Hooks Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False,
    tags=["hooks"]
)

def create_table():
    create_query = "CREATE TABLE IF NOT EXISTS teste_hook(id int)"

    pg_hook = PostgresHook(postgres_conn_id="postgres-postgres")
    pg_hook.run(create_query, autocommit=True)

def insert_data():
    insert_query = "insert into teste_hook values (1)"

    pg_hook = PostgresHook(postgres_conn_id="postgres-postgres")
    pg_hook.run(insert_query, autocommit=True)

def select_data(**kwargs):
    data_query = "select * from teste_hook"

    pg_hook = PostgresHook(postgres_conn_id="postgres-postgres")
    records = pg_hook.get_records(data_query)
    kwargs['ti'].xcom_push(key="query_result", value=records)

def print_result(ti):
    task_instance = ti.xcom_pull(key="query_result", task_ids="select_data_task")
    print("Resultado da consulta")
    for row in task_instance:
        print(row)

create_table_task = PythonOperator(
    task_id="create_table_task",
    python_callable=create_table,
    dag=dag
)

insert_data_task = PythonOperator(
    task_id="insert_data_task",
    python_callable=insert_data,
    dag=dag
)

select_data_task = PythonOperator(
    task_id="select_data_task",
    python_callable=select_data,
    provide_context=True,
    dag=dag
)

print_result_task = PythonOperator(
    task_id="print_result_task",
    python_callable=print_result,
    provide_context=True,
    dag=dag
)

create_table_task >> insert_data_task >> select_data_task >> print_result_task