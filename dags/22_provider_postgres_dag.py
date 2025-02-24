from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator

dag = DAG(
    "database_postgres",
    description="Database(Postgres) Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False,
    tags=["http_sensor"]
)

def print_result(ti):
    task_instance = ti.xcom_pull(task_ids="select_data_task")
    print("Resultado da consulta")
    for row in task_instance:
        print(row)


create_query = "create table if not exists teste(id int)"

create_table_task = PostgresOperator(
    task_id="create_table_task",
    postgres_conn_id='postgres',
    sql=create_query,
    dag=dag
)

insert_query = "insert into teste values (1)"

insert_data_task = PostgresOperator(
    task_id="insert_data_task",
    postgres_conn_id='postgres',
    sql=insert_query,
    dag=dag
)

data_query = "select * from teste"

select_data_task = PostgresOperator(
    task_id="select_data_task",
    postgres_conn_id='postgres',
    sql=data_query,
    dag=dag
)

print_result_task = PythonOperator(
    task_id="print_result_task",
    python_callable=print_result,
    provide_context=True,
    dag=dag
)

create_table_task >> insert_data_task >> select_data_task >> print_result_task