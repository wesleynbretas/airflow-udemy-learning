from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 17),
    'email': ['test@test.com'],
    'email_on_failed' : True,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay': timedelta(seconds=10)
}


dag = DAG(
    'send_email_dag',
    description="Send Email DAG",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 2, 17),
    catchup=False,
    default_view='graph',
    tags=['send_email']

)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag)
task4 = BashOperator(task_id="task4", bash_command="exit 1", dag=dag)
task5 = BashOperator(task_id="task5", bash_command="sleep 5", dag=dag, trigger_rule='none_failed')
task6 = BashOperator(task_id="task6", bash_command="sleep 5", dag=dag, trigger_rule='none_failed')

send_email = EmailOperator(task_id="send_email", 
                        to="wesley.bretas@outlook.com",
                        subject="Airflow Error",
                        html_content="""
                            <h3> Error in DAG. </h3>
                            <p>Dag: send_email </p>


                        """,
                        dag=dag, trigger_rule="one_failed"
                        )

[task1, task2] >> task3 >> task4

task4 >> [task5, task6, send_email]