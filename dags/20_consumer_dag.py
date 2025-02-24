from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

my_dataset = Dataset("/opt/airflow/data/churn_new.csv")

dag = DAG(
    "consumer",
    description="Consumer Dag Example",
    schedule_interval=[my_dataset],
    start_date=datetime(2025, 2, 12),
    catchup=False,
    tags=["datasets"]
)

def my_file():
    df = pd.read_csv("/opt/airflow/data/churn_producer.csv", sep=";")

    df.to_csv("/opt/airflow/data/churn_consumer.csv", sep=";")


consumer_task = PythonOperator(task_id="consumer_task", python_callable=my_file, dag=dag, provide_context=True)

consumer_task