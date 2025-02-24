from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.utils import timezone


dag = DAG(
    "trigger_all_failed_dag",
    description="Trigger All Failed Example",
    schedule_interval="33 21 * * *",
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

task1 = BashOperator(task_id="task1", bash_command="exit 1", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="exit 1", dag=dag)
# this task will only run if a previous task fails
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag, trigger_rule="all_failed")

[task1, task2]  >> task3