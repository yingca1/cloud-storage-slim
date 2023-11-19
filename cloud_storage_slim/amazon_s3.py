import boto3
from cloud_storage_slim import CloudStorage


class AmazonS3Storage(CloudStorage):
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def download(self, bucket_name, remote_blob_path, local_blob_path):
        self.s3_client.download_file(bucket_name, remote_blob_path, local_blob_path)

    def upload(self, bucket_name, local_blob_path, remote_blob_path):
        self.s3_client.upload_file(local_blob_path, bucket_name, remote_blob_path)

    def list_blobs(self, bucket_name, pattern):
        response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=pattern)
        return [item["Key"] for item in response.get("Contents", [])]

    def get_first_blob(self, bucket_name, pattern):
        blobs_list = self.list_blobs(bucket_name, pattern)
        return blobs_list[0] if blobs_list else None
