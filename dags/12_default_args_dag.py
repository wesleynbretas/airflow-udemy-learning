from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 17),
    'email': ['test@test.com'],
    'email_on_failed' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay': timedelta(seconds=10)
}


dag = DAG(
    'default_args_dag',
    description="Default Args DAG",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2025, 2, 17),
    catchup=False,
    default_view='graph',
    tags=['default_args']

)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag, retries=3)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag)

task1 >> task2 >> task3