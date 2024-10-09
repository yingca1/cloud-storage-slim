import os
import importlib
from cloud_storage_slim import CloudStorage


class TorchObjectStorage(CloudStorage):
    def __init__(self) -> None:
        storage_module = importlib.import_module("tos")
        ak = os.getenv("TOS_ACCESS_KEY_ID", None)
        sk = os.getenv("TOS_SECRET_ACCESS_KEY", None)
        endpoint = os.getenv("TOS_ENDPOINT_URL", None)
        region = os.getenv("TOS_DEFAULT_REGION", None)
        self.storage_client = storage_module.TosClientV2(ak, sk, endpoint, region)

    def download(self, bucket_name, remote_blob_path, local_blob_path, **kwargs):
        self.storage_client.download_file(bucket=bucket_name, key=remote_blob_path, file_path=local_blob_path)

    def upload(self, bucket_name, local_blob_path, remote_blob_path, **kwargs):
        self.storage_client.upload_file(bucket_name, remote_blob_path, local_blob_path)

    def list_blobs(self, bucket_name, pattern):
        list_objects = self.storage_client.list_objects(bucket_name, prefix=pattern)
        blobs_list = list_objects.contents
        blobs_list_names = [blob.key for blob in blobs_list]
        return blobs_list_names

    def get_first_blob(self, bucket_name, pattern):
        list_objects = self.storage_client.list_objects(bucket_name, prefix=pattern, max_keys=1)
        blobs_list = list_objects.contents
        if len(blobs_list) == 0:
            return None
        return blobs_list[0].key

    def get_native_client(self):
        return self.storage_client

    def download_uri(self, remote_blob_uri, local_blob_path, **kwargs):
        raise NotImplementedError("Torch Object Storage does not support downloading from URI")

    def upload_uri(self, local_blob_path, remote_blob_uri, **kwargs):
        raise NotImplementedError("Torch Object Storage does not support uploading to URI")
