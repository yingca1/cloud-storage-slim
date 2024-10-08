# Cloud Storage Slim

Make operations across various cloud storage platforms simple.

## Installation

```bash
pip install cloud-storage-slim
```

## Usage

```python
from cloud_storage_slim import CloudStorageSlim

cloud_storage = CloudStorageSlim()
cloud_storage.copyto('gs://bucket1/object1', 'az://bucket2/object2')
```

## Features

- [copyto](https://rclone.org/commands/rclone_copyto/)
- [ls](https://rclone.org/commands/rclone_ls/)

## Supported Cloud Storage

- [x] Google Cloud Storage
- [x] Azure Blob Storage
- [x] AlibabaCloud / Aliyun OSS
- [x] AWS S3

## Credentials

### Google Cloud Storage

- [How Application Default Credentials works](https://cloud.google.com/docs/authentication/application-default-credentials)
- `GOOGLE_APPLICATION_CREDENTIALS`
- [google-cloud-python](https://github.com/googleapis/python-storage)

```bash
pip install google-cloud-storage
```

## Amazon S3

- [Boto3 Configuring credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#environment-variables)
- [Using environment variables](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables)
- `AWS_ENDPOINT_URL_S3`
- `AWS_DEFAULT_REGION`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- [Boto3](https://github.com/boto/boto3)

```bash
pip install boto3
```

### Azure Blob Storage

- [Manage storage account access keys](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys)
- `AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_STORAGE_ACCOUNT_KEY`

```bash
pip install azure-storage-blob azure-identity
```

### AlibabaCloud / Aliyun OSS

- [Configure access credentials](https://www.alibabacloud.com/help/en/oss/developer-reference/python-configuration-access-credentials)
- `OSS_ENDPOINT`
- `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`
- `OSS_SESSION_TOKEN`
- [oss2](https://github.com/aliyun/aliyun-oss-python-sdk)

```bash
pip install oss2
```

### Byteplus / Volcengine - Torch Object Storage

#### S3 Compatible API

- Byteplus [Region and Endpoint](https://docs.byteplus.com/en/docs/tos/docs-region-and-endpoint)
- Byteplus [Compatibility with Amazon S3](https://docs.byteplus.com/en/docs/tos/docs-compatibility-with-amazon-s3)

#### TOC SDK

- `TOC_ENDPOINT_URL`
- `TOC_ACCESS_KEY_ID` `TOC_SECRET_ACCESS_KEY`
- `TOC_DEFAULT_REGION`
- [ve-tos-python-sdk](https://github.com/volcengine/ve-tos-python-sdk)

```bash
pip install tos
```

## Test cases

**before run test cases, you need to prepare the test bucket.**
