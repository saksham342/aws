import boto3
from botocore.config import Config
from botocore import UNSIGNED
from botocore.client import Config as BotocoreConfig

# Disable request signing
unsigned_config = BotocoreConfig(signature_version=UNSIGNED)

# Create the S3 client with no signing
s3 = boto3.client('s3', config=unsigned_config)

bucket_name = 'yoursafetypal'

try:
    # List objects in the S3 bucket without signing the request
    response = s3.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        print(obj['Key'])
except Exception as e:
    print(f'Error: {e}')
