from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.utils import timezone


with DAG(
    "fourth_dag",
    description="Third DAG",
    schedule_interval="33 21 * * *",
    start_date=datetime(2025, 2, 12),
    catchup=False    
) as dag:

    task1 = BashOperator(task_id="task1", bash_command="sleep 5")
    task2 = BashOperator(task_id="task2", bash_command="sleep 5")
    task3 = BashOperator(task_id="task3", bash_command="sleep 5")

task1.set_upstream(task2)
task2.set_upstream(task3)