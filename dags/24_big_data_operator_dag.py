from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

from big_data_operator import BigDataOperator

dag = DAG(
    "big_data_dag",
    description="Big Data Operator DAG",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False,
    tags=["plugins"]
)

var_type_file = "parquet"
big_data_parquet_task = BigDataOperator(
    task_id="big_data_parquet_task",
    path_to_csv_file = "/opt/airflow/data/churn.csv",
    path_to_save_file = f"/opt/airflow/data/churn.{var_type_file}",
    type_file = var_type_file,
    dag=dag
)

var_type_file = "json"
big_data_json_task = BigDataOperator(
    task_id="big_data_json_task",
    path_to_csv_file = "/opt/airflow/data/churn.csv",
    path_to_save_file = f"/opt/airflow/data/churn.{var_type_file}",
    type_file = var_type_file,
    dag=dag
)

big_data_parquet_task >> big_data_json_task