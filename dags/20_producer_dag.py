from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

dag = DAG(
    "producer",
    description="Producer Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False,
    tags=["datasets"]
)

my_dataset = Dataset("/opt/airflow/data/churn_new.csv")

def my_file():
    df = pd.read_csv("/opt/airflow/data/churn.csv", sep=";")

    df.to_csv("/opt/airflow/data/churn_producer.csv", sep=";")


producer_task = PythonOperator(task_id="producer_task", python_callable=my_file, dag=dag, outlets=[my_dataset])

producer_task

