import importlib
import urllib3
from cloud_storage_slim import CloudStorage

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HttpRemoteFile(CloudStorage):
    def __init__(self) -> None:
        storage_module = importlib.import_module("requests")
        self.requests_session = storage_module.Session()

    def download_uri(self,remote_blob_uri, local_blob_path, **kwargs):
        response = self.requests_session.get(remote_blob_uri, stream=True, verify=False)

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

    def get_navite_client(self):
        return self.requests_session
