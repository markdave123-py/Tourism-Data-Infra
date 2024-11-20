from services.config import get_config
from services.extract_from_s3 import extract_from_s3
from services.rds_loader import rds_loader
from services.config import get_config
import logging



def extract_operation(**kwargs):
    s3_bucket = get_config("s3_bucket")
    s3_key = get_config("s3_key")
    return extract_from_s3(s3_bucket, s3_key)

def transform_operation(**kwargs):
    """
    Validate and push raw data for loading if transformation is not needed.
    """
    try:
        # Pull pre_transformed data from the extract_task
        raw_data = kwargs['ti'].xcom_pull(task_ids='extract_task')
        if not raw_data:
            logging.warning("No data received from extract_task.")
            return

        # Push  data to the next task for loading
        kwargs['ti'].xcom_push(key='transformed_batch', value=raw_data)
        logging.info("Raw data pushed directly for loading.")
    except Exception as e:
        logging.error(f"Error in transform_operation: {e}")
        raise


def load_operation(**kwargs):
    try:
        transformed_batch = kwargs['ti'].xcom_pull(task_ids='transform_task', key='transformed_batch')
        if not transformed_batch:
            logging.warning("No data received for loading.")
            return
        rds_loader(transformed_batch)
    except Exception as e:
        logging.error(f"Error in load_operation: {e}")
        raise
