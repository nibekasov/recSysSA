import os

from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta




default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 16),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
    'schedule_interval': '@daily',
}


dag = DAG('preparation', description='ADD DESCRIPTION', default_args=default_args, catchup=False)

prep_operator = PythonOperator(task_id='preparation_task', python_callable=SPLIT, dag=dag)

prep_operator