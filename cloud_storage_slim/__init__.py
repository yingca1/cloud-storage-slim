import os
import uuid
import shutil
import importlib.util
from cloud_storage_slim.utils import (
    parse_path_uri,
    check_scheme,
    check_source_local_file,
    check_dest_local_file,
)


class CloudStorage:
    def download(self, bucket_name, remote_blob_path, local_blob_path):
        raise NotImplementedError

    def upload(self, bucket_name, local_blob_path, remote_blob_path):
        raise NotImplementedError

    def list_blobs(self, bucket_name, pattern):
        raise NotImplementedError

    def get_first_blob(self, bucket_name, pattern):
        raise NotImplementedError


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

    def _setup_tmp_workspace(self):
        tmp_workspace_folder_path = os.path.join(
            os.path.expanduser("~"), ".cloud_storage_slim"
        )
        if not os.path.exists(tmp_workspace_folder_path):
            os.makedirs(tmp_workspace_folder_path)
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
        else:
            raise ValueError(f"Unknown scheme: {scheme}")

    def destroy(self):
        self._teardown_tmp_workspace()
        self.gcs_client = None
        self.az_client = None
        self.oss_client = None

    def _copy_local_to_remote(self, source_path, dest_path):
        local_blob_path = os.path.abspath(source_path)
        scheme, bucket_name, blob_path = parse_path_uri(dest_path)
        client = self._get_client(scheme)
        client.upload(bucket_name, local_blob_path, blob_path)

    def _copy_remote_to_local(self, source_path, dest_path):
        scheme, bucket_name, blob_path = parse_path_uri(source_path)
        client = self._get_client(scheme)
        client.download(bucket_name, blob_path, dest_path)

    def _copy_remote_to_remote(self, source_path, dest_path, filter_options=None):
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
            if filter_options is not None:
                include = filter_options.get("include", None)
                if include is not None:
                    search_path = f"{source_blob_path}{include}"
                    source_blob_path = source_client.get_first_blob(
                        source_bucket_name, search_path
                    )
                    if source_blob_path is None:
                        raise ValueError(
                            f"Cannot find blob with prefix {search_path} from {source_scheme}://{source_bucket_name}"
                        )

            source_client.download(
                source_bucket_name, source_blob_path, local_blob_path
            )

            dest_client.upload(dest_bucket_name, local_blob_path, dest_blob_path)
        finally:
            if os.path.exists(local_blob_path):
                os.remove(local_blob_path)

    def copyto(self, source_path, dest_path, filter_options=None):
        """
        limitaions: only support single file copy right now
        """
        if check_source_local_file(source_path):
            # local to local
            if check_dest_local_file(dest_path):
                shutil.copyfile(source_path, dest_path)
            else:
                check_scheme(dest_path)
                # local to remote
                self._copy_local_to_remote(source_path, dest_path)
        else:
            check_scheme(source_path)
            if check_dest_local_file(dest_path):
                # remote to local
                self._copy_remote_to_local(source_path, dest_path)
            else:
                check_scheme(dest_path)
                # remote to remote
                self._copy_remote_to_remote(source_path, dest_path, filter_options)

    def ls(self, remote_path, include=""):
        scheme, bucket_name, blob_path = parse_path_uri(remote_path)
        client = self._get_client(scheme)
        return client.list_blobs(bucket_name, f"{blob_path}{include}")
