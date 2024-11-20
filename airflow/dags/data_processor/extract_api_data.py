from airflow.exceptions import AirflowException
import logging
from services.config import get_config
from services.s3_uploader import upload_to_s3
from services.api_handler import fetch_data_chuck
from services.transform_s3 import transform_s3_data

def extract_save_to_s3(**context):
    """
    Extract data from an API, transform it, and upload to S3 in batches.
    """
    logger = logging.getLogger("airflow.task")

    try:
        api_url = get_config("api_url")
        s3_bucket = get_config("s3_bucket")
        s3_key = get_config("s3_key")
        batch_size = context.get("batch_size", 100)

        logger.info(f"Starting data extraction from API: {api_url}")
        logger.info(f"Target S3 path: s3://{s3_bucket}/{s3_key}")

        batch = []
        for data_chunk in fetch_data_chuck(api_url):
            batch.extend(data_chunk if isinstance(data_chunk, list) else [data_chunk])

            # Transform and upload in batches
            if len(batch) >= batch_size:
                logger.info(f"Processing and uploading {len(batch)} records...")
                transformed = transform_s3_data(batch)
                upload_to_s3(transformed, s3_bucket, s3_key)
                batch = []  # Clear the batch after upload

        if batch:  # Handle remaining data
            logger.info(f"Processing and uploading final {len(batch)} records...")
            transformed = transform_s3_data(batch)
            upload_to_s3(transformed, s3_bucket, s3_key)

        logger.info("Data extraction and upload completed successfully.")
    except Exception as e:
        logger.error(f"Error during data extraction or upload: {e}")
        raise AirflowException(e)
