import boto3
from botocore.config import Config as BotocoreConfig
from botocore import UNSIGNED
import threading

# Disable request signing
unsigned_config = BotocoreConfig(signature_version=UNSIGNED)

# Create the S3 client with no signing
s3 = boto3.client('s3', config=unsigned_config)

# List of common bucket names to check
common_bucket_names = [
    'test', 'dev', 'production', 'staging', 'static', 
    'images', 'files', 'backup', 'mybucket', 'public'
]

def check_bucket_exists(bucket_name):
    try:
        # Attempt to list objects in the bucket to check its existence
        s3.head_bucket(Bucket=bucket_name)
        print(f'Bucket found: {bucket_name}')
        return True
    except s3.exceptions.NoSuchBucket:
        # Bucket does not exist
        print(f'Bucket does not exist: {bucket_name}')
    except s3.exceptions.ClientError as e:
        # Check for access denied error, which means the bucket exists but is private
        error_code = e.response['Error']['Code']
        if error_code == '403':
            print(f'Bucket exists but access is denied: {bucket_name}')
        else:
            print(f'Error checking bucket {bucket_name}: {e}')
    return False

# Itirate the list of common bucket names using multi threading
for bucket in common_bucket_names:
    threading.Thread(target=check_bucket_exists, args=(bucket,)).start()
