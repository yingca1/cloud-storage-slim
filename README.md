# Cloud Storage Slim

## Principles

- No complex operations, just focus on simple things.
- Inspired by [rclone](https://rclone.org/).

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
- [x] AlibabaCloud / Aliyun OSS: [oss2](https://github.com/aliyun/aliyun-oss-python-sdk)
- [ ] AWS S3

## Credentials

### Google Cloud Storage

- [How Application Default Credentials works](https://cloud.google.com/docs/authentication/application-default-credentials)
- `GOOGLE_APPLICATION_CREDENTIALS`

```bash
pip install google-cloud-storage
```

### Azure Blob Storage

- [Manage storage account access keys
](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys)
- `AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_STORAGE_ACCOUNT_KEY`

```bash
pip install azure-storage-blob azure-identity
```

### AlibabaCloud / Aliyun OSS

- [Configure access credentials](https://www.alibabacloud.com/help/en/oss/developer-reference/python-configuration-access-credentials)
- `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`
- `OSS_SESSION_TOKEN`

```bash
pip install oss2
```

## Test cases

**before run test cases, you need to prepare the test bucket.**
