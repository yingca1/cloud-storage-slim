import importlib
import urllib3
from cloud_storage_slim import CloudStorage

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HttpRemoteFile(CloudStorage):
    def __init__(self) -> None:
        storage_module = importlib.import_module("requests")
        self.requests_session = storage_module.Session()

    def download_uri(self, remote_blob_uri, local_blob_path, **kwargs):
        """
        https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
        """
        enabled_options = ["timeout"]
        download_options = {k: v for k, v in kwargs.items() if k in enabled_options}

        response = self.requests_session.get(remote_blob_uri, stream=True, verify=False, **download_options)

        with open(local_blob_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    def upload_uri(self, local_blob_path, remote_blob_uri, **kwargs):
        with open(local_blob_path, 'rb') as f:
            if "headers" in kwargs:
                headers = kwargs["headers"]
                self.requests_session.headers.update(headers)
            self.requests_session.put(remote_blob_uri, data=f, verify=False)

    def get_native_client(self):
        return self.requests_session

    def download(self, bucket_name, remote_blob_path, local_blob_path, **kwargs):
        raise NotImplementedError("HttpRemoteFile does not support downloading from bucket")
    
    def upload(self, bucket_name, local_blob_path, remote_blob_path, **kwargs):
        raise NotImplementedError("HttpRemoteFile does not support uploading to bucket")
    
    def list_blobs(self, bucket_name, pattern):
        raise NotImplementedError("HttpRemoteFile does not support listing blobs")
    
    def get_first_blob(self, bucket_name, pattern):
        raise NotImplementedError("HttpRemoteFile does not support getting the first blob")
