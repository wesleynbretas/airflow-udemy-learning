from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.models import Variable

dag = DAG(
    "variable_dag",
    description="Variable Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

def read_variable(**context):
    my_variable = Variable.get("my_variable")
    print(f"Variable value is: {my_variable}")


variable_task = PythonOperator(task_id="variable_task", python_callable=read_variable, dag=dag)

variable_task