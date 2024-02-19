import os
import unittest
from cloud_storage_slim import utils

class TestCloudStorageSlim(unittest.TestCase):

    def test_check_dest_local_file(self):
        # Test with a valid local file path
        valid_local_file_path = os.path.abspath(__file__)
        assert utils.check_dest_local_file(valid_local_file_path) == True

        # Test with a local file path that starts with "file://"
        file_uri_local_file_path = f"file:///{valid_local_file_path}"
        assert utils.check_dest_local_file(file_uri_local_file_path) == True

        # Test with a local file path that is actually a directory
        directory_local_file_path = os.path.dirname(valid_local_file_path)
        assert utils.check_dest_local_file(directory_local_file_path) == False

        # Test with a local file path that parent folder does not exist
        non_exist_parent_local_file_path = f"{directory_local_file_path}/non_exist_parent_folder/random-file.txt"
        assert utils.check_dest_local_file(non_exist_parent_local_file_path) == False

    def test_check_http_file(self):
        # Test with a valid http file path
        valid_https_file_path = "https://www.domain.com/random-file.txt"
        assert utils.check_remote_file(valid_https_file_path) == None

        valid_http_file_path = "http://www.domain.com/random-file.txt"
        assert utils.check_remote_file(valid_http_file_path) == None

    def test_parse_path_uri_http_file(self):
        # Test with a valid http file path
        valid_http_file_path = "http://www.domain.com/path/to/random-file.txt"
        assert utils.parse_path_uri(valid_http_file_path) == ("http", "www.domain.com", "path/to/random-file.txt")

        valid_https_file_path = "https://www.domain.com/path/to/random-file.txt"
        assert utils.parse_path_uri(valid_https_file_path) == ("https", "www.domain.com", "path/to/random-file.txt")
    

if __name__ == "__main__":
    unittest.main()
