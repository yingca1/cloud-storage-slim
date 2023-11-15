import importlib
import os
import logging
from cloud_storage_slim import CloudStorage


class AzureStorage(CloudStorage):
    def __init__(self) -> None:
        self.azure_storage_blob = importlib.import_module("azure.storage.blob")
        self.azure_identity = importlib.import_module("azure.identity")

        logging.basicConfig(level=logging.WARNING)
        azure_logger = logging.getLogger("azure")
        azure_logger.setLevel(logging.WARNING)

        storageaccountname = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
        account_url = f"https://{storageaccountname}.blob.core.windows.net"
        default_credential = self.azure_identity.DefaultAzureCredential()
        self.blob_service_client = self.azure_storage_blob.BlobServiceClient(
            account_url, credential=default_credential
        )

    def download(self, container_name, remote_blob_path, local_blob_path):
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, blob=remote_blob_path
        )

        with open(local_blob_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    def upload(self, container_name, local_blob_path, remote_blob_path):
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, blob=remote_blob_path
        )

        with open(local_blob_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def list_blobs(self, container_name, pattern):
        container_client = self.blob_service_client.get_container_client(container_name)
        blobs_list = list(container_client.list_blobs(name_starts_with=pattern))
        return blobs_list

    def get_first_blob(self, container_name, pattern):
        container_client = self.blob_service_client.get_container_client(container_name)
        blobs_list = list(container_client.list_blobs(name_starts_with=pattern))

        if len(blobs_list) == 0:
            return None

        return blobs_list[0].name
