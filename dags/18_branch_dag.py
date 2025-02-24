from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
import random

from datetime import datetime


dag = DAG(
    "branch_dag",
    description="Branch Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

def generate_random_number():
    return random.randint(1, 100)

generate_random_number_task = PythonOperator(
    task_id="generate_random_number_task",
    python_callable=generate_random_number,
    dag=dag
)

def verify_random_number(**context):
    number = context['task_instance'].xcom_pull(task_ids="generate_random_number_task")

    if number % 2 == 0:
        return 'odd_number_task'
    else:
        return 'even_number_task'    

branch_task = BranchPythonOperator(
    task_id="branch_task",
    python_callable=verify_random_number,
    provide_context=True,
    dag=dag
)

odd_number_task = BashOperator(task_id="odd_number_task", bash_command="echo 'Odd Number'", dag=dag)
even_number_task = BashOperator(task_id="even_number_task", bash_command="echo 'Even Number'", dag=dag)

generate_random_number_task >> branch_task
branch_task >> odd_number_task
branch_task >> even_number_task