import s3fs
import pyarrow.parquet as pq
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
import logging
import boto3
from io import BytesIO
import numpy as np

def extract_from_s3(s3_bucket, s3_key):
    """
    Extract Parquet data from S3 using boto3.
    """
    try:
        # Initialize AWS Hook
        s3_hook = AwsBaseHook(aws_conn_id="aws_default", client_type="s3")

        # Retrieve AWS credentials from Airflow connection
        aws_credentials = s3_hook.get_credentials()
        logging.info(f"Using AWS credentials: Access Key: {aws_credentials.access_key}")

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_credentials.access_key,
            aws_secret_access_key=aws_credentials.secret_key,
            region_name=s3_hook._region_name,
        )

        logging.info(f"Attempting to access bucket: {s3_bucket}, key: {s3_key}")

        # Fetch the object from S3
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

        # Read the Parquet file from the response
        buffer = BytesIO(response["Body"].read())
        table = pq.read_table(buffer)
        df = table.to_pandas()

        # Convert DataFrame to JSON serializable dict
        result = df.applymap(
            lambda x: x.tolist() if isinstance(x, np.ndarray) else x
        ).to_dict("records")

        logging.info(f"Successfully read Parquet file: {s3_key}")
        return result

    except Exception as e:
        logging.error(f"Error reading from S3: {e}")
        raise
