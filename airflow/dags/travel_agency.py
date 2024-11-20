import airflow
from airflow import DAG
from airflow.utils.dates import datetime
from airflow.operators.python import PythonOperator
from data_processor.extract_api_data import extract_save_to_s3
from data_processor.load_to_rds import extract_operation, transform_operation, load_operation
from airflow_dbt_python.operators.dbt import DbtRunOperator, DbtTestOperator
from services.config import get_config





with DAG(
    dag_id="travel_agency",
    start_date=datetime(2024, 11, 18),
    schedule_interval=None,
    catchup=False,
    tags=["example"],
) as dag:



    save_to_s3 = PythonOperator(
        task_id="extract_save_to_s3",
        python_callable= extract_save_to_s3
    )

    extract_from_s3 = PythonOperator(
        task_id="extract_from_s3",
        python_callable=extract_operation,
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_operation,
        provide_context=True,
    )

    load_to_rds = PythonOperator(
        task_id="load_to_rds",
        python_callable=load_operation,
        provide_context=True
    )

    dbt_run_modelling = DbtRunOperator(
        task_id="dbt_modelling",
        project_dir="/opt/airflow/dbt/travel_agency",
        profiles_dir="/opt/airflow/.dbt",
        models=["staging", "dimensions", "facts"],
        do_xcom_push=True,
    )


    save_to_s3 >> extract_from_s3 >> transform_data >> load_to_rds >> dbt_run_modelling
