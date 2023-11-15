import os
import importlib
from cloud_storage_slim import CloudStorage


class AlibabaCloudOSS(CloudStorage):
    def __init__(self) -> None:
        self.oss2 = importlib.import_module("oss2")
        self.endpoint = os.environ.get("OSS_ENDPOINT")
        self.auth = self.oss2.ProviderAuth(self.oss2.credentials.EnvironmentVariableCredentialsProvider())

    def download(self, bucket_name, remote_blob_path, local_blob_path):
        bucket = self.oss2.Bucket(self.auth, self.endpoint, bucket_name)
        bucket.get_object_to_file(remote_blob_path, local_blob_path)

    def upload(self, bucket_name, local_blob_path, remote_blob_path):
        bucket = self.oss2.Bucket(self.auth, self.endpoint, bucket_name)
        bucket.put_object_from_file(remote_blob_path, local_blob_path)

    def list_blobs(self, bucket_name, pattern):
        res_blob_list = []
        bucket = self.oss2.Bucket(self.auth, self.endpoint, bucket_name)
        for obj in self.oss2.ObjectIterator(bucket, prefix=pattern):
            if obj.key.startswith(pattern):
                res_blob_list.append(obj.key)
        return res_blob_list

    def get_first_blob(self, bucket_name, pattern):
        bucket = self.oss2.Bucket(self.auth, self.endpoint, bucket_name)
        for obj in self.oss2.ObjectIterator(bucket, prefix=pattern):
            if obj.key.startswith(pattern):
                return obj.key
        return None
