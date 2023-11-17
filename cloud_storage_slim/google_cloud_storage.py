import importlib
from cloud_storage_slim import CloudStorage


class GoogleCloudStorage(CloudStorage):
    def __init__(self) -> None:
        storage_module = importlib.import_module("google.cloud.storage")
        self.storage_client = storage_module.Client()

    def download(self, bucket_name, remote_blob_path, local_blob_path):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(remote_blob_path)

        blob.download_to_filename(local_blob_path)

    def upload(self, bucket_name, local_blob_path, remote_blob_path):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(remote_blob_path)

        blob.upload_from_filename(local_blob_path)

    def list_blobs(self, bucket_name, pattern):
        bucket = self.storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=pattern)
        blobs_list = list(blobs)
        blobs_list_names = [blob.name for blob in blobs_list]
        return blobs_list_names

    def get_first_blob(self, bucket_name, pattern):
        bucket = self.storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=pattern)
        blobs_list = list(blobs)
        if len(blobs_list) == 0:
            return None
        return blobs_list[0].name
