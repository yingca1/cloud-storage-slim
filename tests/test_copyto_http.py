import os
import random
import unittest
from dotenv import load_dotenv

load_dotenv()

from cloud_storage_slim import CloudStorageSlim


class TestCloudStorageSlim(unittest.TestCase):

    def setUp(self) -> None:
        self.test_file_urls = [
            'https://raw.githubusercontent.com/yingca1/cloud-storage-slim/main/README.md',
            'https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png'
        ]
        return super().setUp()

    def test_remote_to_local(self):
        cloud_storage_slim = CloudStorageSlim()
        local_file_path = "tests/test_remote_to_local.txt"
        remote_file_path = self.test_file_urls[0]
        cloud_storage_slim.copyto(remote_file_path, local_file_path)
        self.assertTrue(os.path.exists(local_file_path))
    

if __name__ == "__main__":
    unittest.main()
