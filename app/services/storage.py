import boto3
from botocore.exceptions import ClientError
from app import config

def upload_to_minio(file_path: str, bucket: str, object_name: str):
    s3_client = boto3.client(
        "s3",
        endpoint_url=config.MINIO_ENDPOINT_URL,
        aws_access_key_id=config.MINIO_ACCESS_KEY,
        aws_secret_access_key=config.MINIO_SECRET_KEY,
        config=boto3.session.Config(signature_version="s3v4")
    )
    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except ClientError as e:
        raise RuntimeError(e)