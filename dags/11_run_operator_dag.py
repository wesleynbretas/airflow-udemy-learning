from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.operators.dagrun_operator import TriggerDagRunOperator

dag = DAG(
    "call_run_operator_dag",
    description="Group Task Dag Example",
    schedule_interval="33 21 * * *",
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag)
task2 = TriggerDagRunOperator(task_id="run_dag_task", trigger_dag_id="run_operator_dag", dag=dag)

task1 >> task2