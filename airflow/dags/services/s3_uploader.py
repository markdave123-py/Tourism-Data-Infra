import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import s3fs
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def upload_to_s3(data, bucket_name, key):


    s3_hook = S3Hook(aws_conn_id="aws_default")

    s3 = s3fs.S3FileSystem(client_kwargs={
        "aws_access_key_id": s3_hook.get_credentials().access_key,
        "aws_secret_access_key": s3_hook.get_credentials().secret_key,
        "region_name": s3_hook._region_name,
    })

    df = pd.DataFrame(data)

    table = pa.Table.from_pandas(df)

    s3_path = f"s3://{bucket_name}/{key}"

    with s3.open(s3_path, "wb") as f:

        pq.write_table(table, f)

