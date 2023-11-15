# Cloud Storage Slim

## Principles

- No complex operations, just basic operations.
- Follow rclone naming conventions.

## Features

- [copyto](https://rclone.org/commands/rclone_copyto/)
- [copy](https://rclone.org/commands/rclone_copy/)

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

- [Sign in and connect your app code to Azure using DefaultAzureCredential](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli#sign-in-and-connect-your-app-code-to-azure-using-defaultazurecredential)
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
