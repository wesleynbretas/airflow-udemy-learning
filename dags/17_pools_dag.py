from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG(
    "pool_dag",
    description="Pools Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag, pool="my_pool")
task2 = BashOperator(task_id="task2", bash_command="sleep 20", dag=dag, pool="my_pool", priority_weight=5)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag, pool="my_pool")
task4 = BashOperator(task_id="task4", bash_command="sleep 5", dag=dag, pool="my_pool", priority_weight=10)