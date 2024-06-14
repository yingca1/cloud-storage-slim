import os
import requests
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
        remote_file_path = 'https://file-examples.com/storage/fe3cb26995666504a8d6180/2017/10/file_example_JPG_1MB.jpg'
        local_file_path = "./file_example_JPG_1MB.jpg"
        cloud_storage_slim.copyto(remote_file_path, local_file_path, predefined_acl="public-read", timeout=(3.05, 27))
        self.assertTrue(os.path.exists(local_file_path))

    def test_http_connect_timeout(self):
        """
        https://httpstat.us/200?sleep=1000
        """
        cloud_storage_slim = CloudStorageSlim()
        remote_file_path = 'https://not-exists-example.com'
        local_file_path = "./test_http_timeout.txt"
        with self.assertRaises(requests.exceptions.ConnectionError):
            cloud_storage_slim.copyto(remote_file_path, local_file_path, timeout=3)

    def test_http_read_timeout(self):
        cloud_storage_slim = CloudStorageSlim()
        remote_file_path = 'https://httpstat.us/200?sleep=50000'
        local_file_path = "./test_http_timeout.txt"

        with self.assertRaises(requests.exceptions.ReadTimeout):
            cloud_storage_slim.copyto(remote_file_path, local_file_path, timeout=(3.05, 5))


if __name__ == "__main__":
    unittest.main()
