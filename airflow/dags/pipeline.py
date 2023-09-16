import logging

from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from scripts.data_prep.prepare_split import split_train_test
import os


def SPLIT():
    data_path = f'{os.path.abspath(os.path.dirname(__file__))}/scripts/data/preprocessed_data/interactions.parquet'
    split_train_test(data_path)



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