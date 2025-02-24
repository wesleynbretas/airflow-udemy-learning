from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

dag = DAG(
    "dummy_dag",
    description="Dummy Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag)
task4 = BashOperator(task_id="task4", bash_command="sleep 5", dag=dag)
task5 = BashOperator(task_id="task5", bash_command="sleep 5", dag=dag)

task_dummy = DummyOperator(task_id="task_dummy", dag=dag)

[task1, task2, task3] >> task_dummy >> [task4, task5]

