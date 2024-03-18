from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from yahoo_data import run_yahoo_etl



default_args = {
    'owner': 'Deepak',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 25),
    'email': ['deepak@mquestgroup.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'yahoo_dags',
    default_args=default_args,
    description='Our first Yahoo DAG with ETL process!',
    schedule_interval=timedelta(hours=1), 
)

run_etl = PythonOperator(
    task_id='yahoo_api_etl',
    python_callable=run_yahoo_etl,
    dag=dag,
)

run_etl