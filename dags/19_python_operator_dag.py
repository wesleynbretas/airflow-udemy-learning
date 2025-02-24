from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import statistics as sts

dag = DAG(
    "python_operator",
    description="Python Operator Dag Example",
    schedule_interval=None,
    start_date=datetime(2025, 2, 12),
    catchup=False    
)

def data_cleaner():
    df = pd.read_csv("/opt/airflow/data/churn.csv", sep=";")
    df.columns = ["id", "score", "state", "gender", "age", "patrimony", "balance", "product", "has_credit_card", "is_active", "salary", "is_churn"]

    salary_median = sts.median(df["salary"])
    
    df["salary"].fillna(salary_median, inplace=True)

    df["gender"].fillna('Masculino', inplace=True)

    median_age = sts.median(df['age'])

    df.loc[(df["age"] < 0) | (df["age"] > 120), "age"] = median_age

    df.drop_duplicates(subset="id", keep="first", inplace=True)

    df.to_csv("/opt/airflow/data/churn_clean.csv", sep=";", index=False)


task_operator = PythonOperator(task_id="task_operator", python_callable=data_cleaner, dag=dag)

task_operator
