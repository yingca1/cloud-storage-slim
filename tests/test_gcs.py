import os
import unittest
from dotenv import load_dotenv

load_dotenv()

from cloud_storage_slim import CloudStorageSlim


class TestCloudStorageSlim(unittest.TestCase):
    def test_upload_file_with_acl_public_read(self):
        """
        https://cloud.google.com/storage/docs/access-control/lists#predefined-acl

        private
        publicRead / public-read
        publicReadWrite / public-read-write
        authenticatedRead / authenticated-read
        bucketOwnerRead / bucket-owner-read
        bucketOwnerFullControl / bucket-owner-full-control
        """
        cloud_storage_slim = CloudStorageSlim()
        test_bucket_gs = os.environ.get("TEST_BUCKET_GS")
        local_file_path = "tests/test_file_public_read.txt"
        if not os.path.exists(local_file_path):
            with open(local_file_path, "w") as file:
                file.write("this is a test file")
        remote_file_path = f"gs://{test_bucket_gs}/test_file_public_read.txt"
        cloud_storage_slim.copyto(
            local_file_path, remote_file_path, predefined_acl="public-read"
        )
        gcs_client = cloud_storage_slim.get_client("gs")
        retrieved_blob = gcs_client.bucket(test_bucket_gs).blob(
            "test_file_public_read.txt"
        )
        acl_entries = retrieved_blob.acl
        self.assertTrue(
            any(
                entry["role"] == "READER" and entry["entity"] == "allUsers"
                for entry in acl_entries
            )
        )

    def test_upload_file_with_acl_private(self):
        cloud_storage_slim = CloudStorageSlim()
        test_bucket_gs = os.environ.get("TEST_BUCKET_GS")
        local_file_path = "tests/test_file_private.txt"
        if not os.path.exists(local_file_path):
            with open(local_file_path, "w") as file:
                file.write("this is a test file")
        remote_file_path = f"gs://{test_bucket_gs}/test_file_private.txt"
        cloud_storage_slim.copyto(
            local_file_path, remote_file_path, predefined_acl="private"
        )

        gcs_client = cloud_storage_slim.get_client("gs")
        retrieved_blob = gcs_client.bucket(test_bucket_gs).blob("test_file_private.txt")
        acl_entries = retrieved_blob.acl
        self.assertTrue(
            all(
                entry["role"] != "READER" and entry["entity"] != "allUsers"
                for entry in acl_entries
            )
        )


if __name__ == "__main__":
    unittest.main()
