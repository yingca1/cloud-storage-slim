import os
import random
import unittest
from dotenv import load_dotenv

load_dotenv()

from cloud_storage_slim import CloudStorageSlim


class TestCloudStorageSlim(unittest.TestCase):
    def get_gs_test_file_path_prefix(self, prefix=""):
        test_bucket_gs = os.environ.get("TEST_BUCKET_GS")
        return os.path.join(f"gs://{test_bucket_gs}", prefix)

    def get_s3_test_file_path_prefix(self, prefix=""):
        test_bucket_s3 = os.environ.get("TEST_BUCKET_S3")
        return os.path.join(f"s3://{test_bucket_s3}", prefix)

    def get_az_test_file_path_prefix(self, prefix=""):
        test_bucket_az = os.environ.get("TEST_BUCKET_AZ")
        return os.path.join(f"az://{test_bucket_az}", prefix)

    def get_oss_test_file_path_prefix(self, prefix=""):
        test_bucket_oss = os.environ.get("TEST_BUCKET_OSS")
        return os.path.join(f"oss://{test_bucket_oss}", prefix)

    def get_local_test_file_path_prefix(self, prefix=""):
        return os.path.join(self.test_working_dir, prefix)

    def get_random_remote_file_path(self):
        random_scheme = random.choice(["gs", "az", "oss"])
        return self.get_dest_test_file_path(random_scheme, "local", random_scheme)

    def create_local_file(
        self, local_file_path, file_content="this is cloud_storage_slim test file"
    ):
        with open(local_file_path, "w") as file:
            file.write(file_content)

    def create_remote_file(self, scheme, file_content=""):
        file_name = f"test_file_from_{scheme}.txt"
        file_content = f"this is cloud_storage_slim test file from {scheme}"
        if scheme == "gs":
            local_file_path = os.path.join(
                self.get_local_test_file_path_prefix(), file_name
            )
            self.create_local_file(local_file_path, file_content)
            remote_file_path = os.path.join(
                self.get_gs_test_file_path_prefix(), file_name
            )
            self.cloud_storage_slim.copyto(local_file_path, remote_file_path)
            return remote_file_path
        elif scheme == "az":
            local_file_path = os.path.join(
                self.get_local_test_file_path_prefix(), file_name
            )
            self.create_local_file(local_file_path, file_content)
            remote_file_path = os.path.join(
                self.get_az_test_file_path_prefix(), file_name
            )
            self.cloud_storage_slim.copyto(self.test_file_path, remote_file_path)
            return remote_file_path
        elif scheme == "oss":
            local_file_path = os.path.join(
                self.get_local_test_file_path_prefix(), file_name
            )
            self.create_local_file(local_file_path, file_content)
            remote_file_path = os.path.join(
                self.get_oss_test_file_path_prefix(), file_name
            )
            self.cloud_storage_slim.copyto(self.test_file_path, remote_file_path)
            return remote_file_path
        elif scheme == "s3":
            local_file_path = os.path.join(
                self.get_local_test_file_path_prefix(), file_name
            )
            self.create_local_file(local_file_path, file_content)
            remote_file_path = os.path.join(
                self.get_s3_test_file_path_prefix(), file_name
            )
            self.cloud_storage_slim.copyto(self.test_file_path, remote_file_path)
            return remote_file_path

    def get_dest_test_file_path(self, scheme, source, dest):
        path_prefix = ""
        if scheme == "gs":
            path_prefix = self.get_gs_test_file_path_prefix()
        elif scheme == "s3":
            path_prefix = self.get_s3_test_file_path_prefix()
        elif scheme == "az":
            path_prefix = self.get_az_test_file_path_prefix()
        elif scheme == "oss":
            path_prefix = self.get_oss_test_file_path_prefix()
        elif scheme == "file" or scheme == "local":
            path_prefix = self.get_local_test_file_path_prefix()

        return os.path.join(path_prefix, f"test_file_{source}_{dest}.txt")

    def setUp(self):
        self.cloud_storage_slim = CloudStorageSlim()
        self.test_working_dir = os.path.join(os.getcwd(), ".cache")
        if not os.path.exists(self.test_working_dir):
            os.mkdir(self.test_working_dir)

        self.test_file_path = "test_file.txt"
        self.create_local_file(self.test_file_path)

    def tearDown(self):
        self.cloud_storage_slim.destroy()
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_copyto_local_to_local(self):
        source_path = self.test_file_path
        dest_path = "test_file_copy_from_local.txt"
        self.cloud_storage_slim.copyto(source_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))
        self.assertEqual(os.path.getsize(source_path), os.path.getsize(dest_path))

    def test_copyto_local_to_remote(self):
        source_path = self.test_file_path
        dest_path_gs = self.get_dest_test_file_path("gs", "local", "gs")
        dest_path_s3 = self.get_dest_test_file_path("s3", "local", "s3")
        dest_path_az = self.get_dest_test_file_path("az", "local", "az")
        dest_path_oss = self.get_dest_test_file_path("oss", "local", "oss")
        # gs
        self.cloud_storage_slim.copyto(source_path, dest_path_gs)
        list_blobs = self.cloud_storage_slim.ls(dest_path_gs)
        self.assertEqual(len(list_blobs), 1)
        
        # s3
        self.cloud_storage_slim.copyto(source_path, dest_path_s3)
        list_blobs = self.cloud_storage_slim.ls(dest_path_s3)
        self.assertEqual(len(list_blobs), 1)

        # az
        self.cloud_storage_slim.copyto(source_path, dest_path_az)
        list_blobs = self.cloud_storage_slim.ls(dest_path_az)
        self.assertEqual(len(list_blobs), 1)

        # oss
        self.cloud_storage_slim.copyto(source_path, dest_path_oss)
        list_blobs = self.cloud_storage_slim.ls(dest_path_oss)
        self.assertEqual(len(list_blobs), 1)

    def test_copyto_remote_to_remote(self):
        source_path_gs = self.create_remote_file("gs")
        source_path_az = self.create_remote_file("az")
        source_path_oss = self.create_remote_file("oss")

        dest_path_gs_az = self.get_dest_test_file_path("az", "gs", "az")
        self.cloud_storage_slim.copyto(source_path_gs, dest_path_gs_az)
        list_blobs = self.cloud_storage_slim.ls(dest_path_gs_az)
        self.assertEqual(len(list_blobs), 1)

        dest_path_gs_s3 = self.get_dest_test_file_path("s3", "gs", "s3")
        self.cloud_storage_slim.copyto(source_path_gs, dest_path_gs_s3)
        list_blobs = self.cloud_storage_slim.ls(dest_path_gs_s3)
        self.assertEqual(len(list_blobs), 1)

        dest_path_gz_oss = self.get_dest_test_file_path("oss", "gs", "oss")
        self.cloud_storage_slim.copyto(source_path_gs, dest_path_gz_oss)
        list_blobs = self.cloud_storage_slim.ls(dest_path_gz_oss)
        self.assertEqual(len(list_blobs), 1)

        dest_path_az_gs = self.get_dest_test_file_path("gs", "az", "gs")
        self.cloud_storage_slim.copyto(source_path_az, dest_path_az_gs)
        list_blobs = self.cloud_storage_slim.ls(dest_path_az_gs)
        self.assertEqual(len(list_blobs), 1)

        dest_path_oss_gs = self.get_dest_test_file_path("gs", "oss", "gs")
        self.cloud_storage_slim.copyto(source_path_oss, dest_path_oss_gs)
        list_blobs = self.cloud_storage_slim.ls(dest_path_oss_gs)
        self.assertEqual(len(list_blobs), 1)

    def test_copyto_remote_to_local(self):
        source_path_gs = self.create_remote_file("gs")
        source_path_s3 = self.create_remote_file("s3")
        source_path_az = self.create_remote_file("az")
        source_path_oss = self.create_remote_file("oss")

        dest_path_gz_local = self.get_dest_test_file_path("local", "gs", "local")
        self.cloud_storage_slim.copyto(source_path_gs, dest_path_gz_local)
        self.assertTrue(os.path.exists(dest_path_gz_local))

        dest_path_s3_local = self.get_dest_test_file_path("local", "s3", "local")
        self.cloud_storage_slim.copyto(source_path_s3, dest_path_s3_local)
        self.assertTrue(os.path.exists(dest_path_s3_local))        

        dest_path_az_local = self.get_dest_test_file_path("local", "az", "local")
        self.cloud_storage_slim.copyto(source_path_az, dest_path_az_local)
        self.assertTrue(os.path.exists(dest_path_az_local))

        dest_path_oss_local = self.get_dest_test_file_path("local", "oss", "local")
        self.cloud_storage_slim.copyto(source_path_oss, dest_path_oss_local)
        self.assertTrue(os.path.exists(dest_path_oss_local))

    def test_copyto_invalid_source_path(self):
        source_path = os.path.join(
            self.get_local_test_file_path_prefix(), "invalid_file.txt"
        )
        dest_path = self.get_random_remote_file_path()
        with self.assertRaises(Exception):
            self.cloud_storage_slim.copyto(source_path, dest_path)

    def test_copyto_invalid_dest_path(self):
        source_path = self.test_file_path

        dest_path_gs = "gs://invalid_bucket/invalid_file.txt"
        with self.assertRaises(Exception):
            self.cloud_storage_slim.copyto(source_path, dest_path_gs)

        dest_path_az = "az://invalid_container/invalid_file.txt"
        with self.assertRaises(Exception):
            self.cloud_storage_slim.copyto(source_path, dest_path_az)

        dest_path_oss = "oss://invalid_bucket/invalid_file.txt"
        with self.assertRaises(Exception):
            self.cloud_storage_slim.copyto(source_path, dest_path_oss)


if __name__ == "__main__":
    unittest.main()
