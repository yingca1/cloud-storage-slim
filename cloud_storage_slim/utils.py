import os
import re
from urllib.parse import urlparse


def check_scheme(path_uri):
    path_scheme = urlparse(path_uri).scheme
    if path_scheme == "":
        raise ValueError(f"Invalid path uri: {path_uri}")
    if ["gs", "s3", "gcs", "az", "oss"].count(path_scheme) == 0:
        raise ValueError(f"Unsupported scheme: {path_scheme}")


def check_source_local_file(input_path):
    return (os.path.exists(input_path) and os.path.isfile(input_path)) or urlparse(
        input_path
    ).scheme == "file"


def check_dest_local_file(input_path):
    if re.search(r'[<>:"|?*]', input_path):
        return False

    if input_path.startswith("file://"):
        input_path = urlparse(input_path).path

    input_path = os.path.expanduser(input_path)
    input_path = os.path.abspath(input_path)

    if os.path.isdir(input_path):
        return False

    parent_dir = os.path.dirname(input_path)

    if not os.path.exists(parent_dir) or not os.access(parent_dir, os.W_OK):
        return False

    return True


def parse_path_uri(storage_bucket):
    parsed_url = urlparse(storage_bucket)
    scheme = parsed_url.scheme
    bucket_name = parsed_url.netloc
    blob_path = parsed_url.path.lstrip("/")
    return scheme, bucket_name, blob_path
