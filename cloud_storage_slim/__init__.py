import os
import uuid
import shutil
import importlib.util
from abc import ABC, abstractmethod
from cloud_storage_slim.utils import (
    parse_path_uri,
    check_remote_file,
    check_source_local_file,
    check_dest_local_file,
)

class CloudStorage(ABC):
    @abstractmethod
    def download(self, bucket_name, remote_blob_path, local_blob_path, **kwargs):
        pass

    @abstractmethod
    def upload(self, bucket_name, local_blob_path, remote_blob_path, **kwargs):
        pass

    @abstractmethod
    def download_uri(self, remote_blob_uri, local_blob_path, **kwargs):
        pass

    @abstractmethod
    def upload_uri(self, local_blob_path, remote_blob_uri, **kwargs):
        pass

    @abstractmethod
    def list_blobs(self, bucket_name, pattern):
        pass

    @abstractmethod
    def get_first_blob(self, bucket_name, pattern):
        pass

    @abstractmethod
    def get_native_client(self):
        pass


class CloudStorageSlim:
    def __init__(self) -> None:
        package_spec = importlib.util.find_spec("dotenv")
        if package_spec is not None:
            dotenv_module = importlib.util.module_from_spec(package_spec)
            package_spec.loader.exec_module(dotenv_module)
            dotenv_module.load_dotenv()

        self.gcs_client = None
        self.az_client = None
        self.oss_client = None
        self.s3_client = None
        self.http_client = None
        self.tos_client = None

    def _setup_tmp_workspace(self):
        tmp_workspace_folder_path = os.path.join(
            os.path.expanduser("~"), ".cloud_storage_slim"
        )
        if not os.path.exists(tmp_workspace_folder_path):
            os.makedirs(tmp_workspace_folder_path, exist_ok=True)
        return tmp_workspace_folder_path

    def _teardown_tmp_workspace(self):
        tmp_workspace_folder_path = os.path.join(
            os.path.expanduser("~"), ".cloud_storage_slim"
        )
        if os.path.exists(tmp_workspace_folder_path):
            shutil.rmtree(tmp_workspace_folder_path)

    def _get_client(self, scheme) -> CloudStorage:
        if scheme == "gs" or scheme == "gcs":
            if self.gcs_client is None:
                from .google_cloud_storage import GoogleCloudStorage
                self.gcs_client = GoogleCloudStorage()
            return self.gcs_client
        elif scheme == "az":
            if self.az_client is None:
                from .azure_storage import AzureStorage
                self.az_client = AzureStorage()
            return self.az_client
        elif scheme == "oss":
            if self.oss_client is None:
                from .alibaba_cloud_oss import AlibabaCloudOSS
                self.oss_client = AlibabaCloudOSS()
            return self.oss_client
        elif scheme == "s3":
            if self.s3_client is None:
                from .amazon_s3 import AmazonS3Storage
                self.s3_client = AmazonS3Storage()
            return self.s3_client
        elif scheme == "tos":
            if self.tos_client is None:
                from .byteplus_torch_object_storage import TorchObjectStorage
                self.tos_client = TorchObjectStorage()
            return self.tos_client
        elif scheme == "http" or scheme == "https":
            from .http_client import HttpRemoteFile
            self.http_client = HttpRemoteFile()
            return self.http_client
        else:
            raise ValueError(f"Unknown scheme: {scheme}")

    def get_client(self, scheme):
        return self._get_client(scheme).get_native_client()

    def destroy(self):
        self._teardown_tmp_workspace()
        self.gcs_client = None
        self.az_client = None
        self.oss_client = None
        self.s3_client = None
        self.tos_client = None

    def _copy_local_to_remote(self, source_path, dest_path, **kwargs):
        local_blob_path = os.path.abspath(source_path)
        scheme, bucket_name, blob_path = parse_path_uri(dest_path)
        client = self._get_client(scheme)
        if scheme == 'http' or scheme == 'https':
            client.upload_uri(local_blob_path, dest_path, **kwargs)
        else:
            client.upload(bucket_name, local_blob_path, blob_path, **kwargs)

    def _copy_remote_to_local(self, source_path, dest_path, **kwargs):
        scheme, bucket_name, blob_path = parse_path_uri(source_path)
        client = self._get_client(scheme)
        if scheme == 'http' or scheme == 'https':
            client.download_uri(source_path, dest_path, **kwargs)
        else:
            client.download(bucket_name, blob_path, dest_path, **kwargs)

    def _copy_remote_to_remote(self, source_path, dest_path, **kwargs):
        source_scheme, source_bucket_name, source_blob_path = parse_path_uri(
            source_path
        )
        source_client = self._get_client(source_scheme)

        dest_scheme, dest_bucket_name, dest_blob_path = parse_path_uri(dest_path)
        dest_client = self._get_client(dest_scheme)

        tmp_workspace_folder_path = self._setup_tmp_workspace()

        unique_local_filename = str(uuid.uuid4())
        local_blob_path = os.path.join(tmp_workspace_folder_path, unique_local_filename)

        try:
            if 'filter_options' in kwargs:
                include = kwargs['filter_options'].get('include', None)
                if include is not None:
                    search_path = f"{source_blob_path}{include}"
                    source_blob_path = source_client.get_first_blob(
                        source_bucket_name, search_path
                    )
                    if source_blob_path is None:
                        raise ValueError(
                            f"Cannot find blob with prefix {search_path} from {source_scheme}://{source_bucket_name}"
                        )

            if source_scheme == 'http' or source_scheme == 'https':
                source_client.download_uri(
                    source_path, local_blob_path, **kwargs
                )
            else:
                source_client.download(
                    source_bucket_name, source_blob_path, local_blob_path, **kwargs
                )

            if dest_scheme == 'http' or dest_scheme == 'https':
                dest_client.upload_uri(local_blob_path, dest_path, **kwargs)
            else:
                dest_client.upload(dest_bucket_name, local_blob_path, dest_blob_path, **kwargs)
        finally:
            if os.path.exists(local_blob_path):
                os.remove(local_blob_path)

    def copyto(self, source_path, dest_path, **kwargs):
        """
        limitaions: only support single file copy right now
        """
        if check_source_local_file(source_path): # source is local file
            if check_dest_local_file(dest_path):
                # dest is local file
                # local to local
                shutil.copyfile(source_path, dest_path)
            else:
                check_remote_file(dest_path) # dest should be valid remote file
                # local to remote
                self._copy_local_to_remote(source_path, dest_path, **kwargs)
        else:
            check_remote_file(source_path) # source should be valid remote file

            if check_dest_local_file(dest_path):
                # dest is local file
                # remote to local
                self._copy_remote_to_local(source_path, dest_path, **kwargs)
            else:
                check_remote_file(dest_path) # dest should be valid remote file
                # remote to remote
                self._copy_remote_to_remote(source_path, dest_path, **kwargs)

    def ls(self, remote_path, include=""):
        scheme, bucket_name, blob_path = parse_path_uri(remote_path)
        client = self._get_client(scheme)
        return client.list_blobs(bucket_name, f"{blob_path}{include}")
