# import logging
# # from pathlib import Path
# # import sys
# # sys.path.append(str(Path(__file__).parent.parent.parent))
# #
#
# from airflow.operators.python import PythonOperator
# from airflow import DAG
# from datetime import datetime, timedelta
#
# def PREPARE():
#     from pathlib import Path
#     import sys
#     sys.path.append(str(Path(__file__).parent.parent.parent))
#
#     from data_prep.data_preprocessing import \
#         load_csv_from_path \
#         , rename_columns \
#         , sampling \
#         , remove_brackets \
#         , drop_nan_values \
#         , check_data_types \
#         , remove_reg_event \
#         , add_session_feature
#
#     interactions = load_csv_from_path()
#
#     # interactions = rename_columns(interactions)
#     # interactions = sampling(interactions)
#     # interactions = remove_brackets(interactions)
#     # interactions = drop_nan_values(interactions)
#     # interactions = check_data_types(interactions)
#     # interactions = remove_reg_event(interactions)
#     # interactions = add_session_feature(interactions)
#
#     # path = r"C:\Users\qwerty\Documents\GitHub\recSysSoA\data\preprocessed_data\interactions.parquet"
#     # interactions.repartition(1).write.format("parquet").mode("overwrite").save(path)
#
#
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2023, 9, 16),
#     'email': ['airflow@example.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=30),
#     'schedule_interval': '@daily',
# }
#
#
# dag = DAG('preparation', description='ADD DESCRIPTION', default_args=default_args, catchup=False)
#
# prep_operator = PythonOperator(task_id='preparation_task', python_callable=PREPARE, dag=dag)
#
# prep_operator