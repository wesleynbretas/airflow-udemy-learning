from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime
import pandas as pd

import requests

dag = DAG(
    "http_sensor",
    description="HTTP Sensor Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False,
    tags=["http_sensor"]
)

def query_api():
    response = requests.get("https://goweather.herokuapp.com/weather/Itu")
    print(response.text)

check_api = HttpSensor(
    task_id="check_api",
    http_conn_id="restapi-goweather",
    endpoint="entries",
    poke_interval=5,
    timeout=20,
    dag=dag
)

process_data = PythonOperator(task_id="process_data", python_callable=query_api, dag=dag)

check_api >> process_data

