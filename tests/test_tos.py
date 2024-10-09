import os
import unittest
from dotenv import load_dotenv

load_dotenv()

from cloud_storage_slim import CloudStorageSlim


class TestCloudStorageSlim(unittest.TestCase):

    def test_upload_file(self):
        """
        https://docs.byteplus.com/en/docs/tos/docs-region-and-endpoint
        https://docs.byteplus.com/en/docs/tos/docs-compatibility-with-amazon-s3
        """
        cloud_storage_slim = CloudStorageSlim()
        bucket_name = os.environ.get("TEST_BUCKET_TOS")
        object_key = "test_file_public_read.txt"

        local_file_path = f"tests/{object_key}"
        if not os.path.exists(local_file_path):
            with open(local_file_path, "w") as file:
                file.write("this is a test file")
        remote_file_path = f"tos://{bucket_name}/{object_key}"
        cloud_storage_slim.copyto(local_file_path, remote_file_path)
        storage_client = cloud_storage_slim.get_client("tos")
        
        head_object = storage_client.head_object(bucket_name, object_key)
        self.assertIsNotNone(head_object.etag)
        self.assertIsNotNone(head_object.last_modified)
        self.assertGreater(head_object.content_length, 0)
        self.assertIsNotNone(head_object.object_type)
        self.assertIsNotNone(head_object.hash_crc64_ecma)

    def test_download_file(self):
        cloud_storage_slim = CloudStorageSlim()
        bucket_name = os.environ.get("TEST_BUCKET_TOS")
        object_key = "test_file_public_read.txt"
        local_file_path = f"tests/{object_key}_downloaded"
        remote_file_path = f"tos://{bucket_name}/{object_key}"
        cloud_storage_slim.copyto(remote_file_path, local_file_path)
        self.assertTrue(os.path.exists(local_file_path))
        os.remove(local_file_path)


    def test_list_objects(self):
        cloud_storage_slim = CloudStorageSlim()
        bucket_name = os.environ.get("TEST_BUCKET_TOS")
        object_key = "test_file_public_read.txt"
        remote_file_pattern = f"tos://{bucket_name}/{object_key}"
        
        object_keys = cloud_storage_slim.ls(remote_file_pattern)
        
        self.assertIsInstance(object_keys, list)
        self.assertGreater(len(object_keys), 0)
        self.assertIn(object_key, [key for key in object_keys])

if __name__ == "__main__":
    unittest.main()
