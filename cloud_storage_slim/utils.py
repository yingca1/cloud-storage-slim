import os
import re
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def check_remote_file(path_uri):
    path_scheme = urlparse(path_uri).scheme
    if path_scheme == "":
        raise ValueError(f"Invalid path uri: {path_uri}")
    if ["gs", "s3", "gcs", "az", "oss", "tos", "http", "https"].count(path_scheme) == 0:
        raise ValueError(f"Unsupported scheme: {path_scheme}")


def check_source_local_file(input_path):
    return (os.path.exists(input_path) and os.path.isfile(input_path)) or urlparse(
        input_path
    ).scheme == "file"


def check_dest_local_file(input_path):
    if input_path.startswith("file://"):
        input_path = urlparse(input_path).path

    input_path = os.path.abspath(os.path.expanduser(input_path))

    parent_dir, filename = os.path.split(input_path)

    invalid_chars_pattern = r'[<>:"|?*\x00]' if os.name == 'nt' else r'[\x00]'

    if re.search(invalid_chars_pattern, filename):
        logger.info(f"filename: [{filename}] contains invalid characters: {invalid_chars_pattern}")
        return False

    if os.path.isdir(input_path):
        logger.info(f"Path: [{input_path}] is a directory, not a file")
        return False

    if not os.path.exists(parent_dir):
        logger.info(f"The parent directory of Path: [{input_path}] does not exist")
        return False

    if not os.access(parent_dir, os.W_OK):
        logger.info(f"The parent directory: [{parent_dir}] is not writable")
        return False

    return True


def parse_path_uri(storage_bucket):
    parsed_url = urlparse(storage_bucket)
    scheme = parsed_url.scheme
    bucket_name = parsed_url.netloc
    blob_path = parsed_url.path.lstrip("/")
    return scheme, bucket_name, blob_path
