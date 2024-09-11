import boto3
from botocore.config import Config as BotocoreConfig
from botocore import UNSIGNED
import random
import string
import threading

# Disable request signing
unsigned_config = BotocoreConfig(signature_version=UNSIGNED)

# Create the S3 client with no signing
s3 = boto3.client('s3', config=unsigned_config)

# List of common bucket names to check
common_bucket_names = [
    'rfd',
    'tempdev',
    'ugis-dev',
    'kfs-test',
    'yoursafetypal',
    'davis1',
    'corporate-img',
    'dev-m3s',
    '2dm',
    'lesson-time',
    'nortesys',
    'beta-switch',
    'evstest'
]



def generate_random_string(length=8):
    """Generate a random string for object naming."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_upload(bucket_name):
    """Test upload permission by attempting to upload a small file."""
    test_object_name = f'test-object-{generate_random_string()}.txt'
    try:
        s3.put_object(Bucket=bucket_name, Key=test_object_name, Body=b'This is a test upload.')
        print(f'Successfully uploaded object to bucket: {bucket_name}')
        return test_object_name
    except s3.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print(f'Upload access denied for bucket: {bucket_name}')
        else:
            print(f'Error uploading to bucket {bucket_name}: {e}')
    return None

def test_delete(bucket_name, object_name):
    """Test delete permission by attempting to delete an object."""
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f'Successfully deleted object from bucket: {bucket_name}')
    except s3.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print(f'Delete access denied for bucket: {bucket_name}')
        else:
            print(f'Error deleting object from bucket {bucket_name}: {e}')

def check_bucket_permissions(bucket_name):
    """Check both upload and delete permissions for a bucket."""
    object_name = test_upload(bucket_name)
    if object_name:
        # Test delete only if upload was successful
        test_delete(bucket_name, object_name)

# Iterate over the list of common bucket names
for bucket in common_bucket_names:
    print(f"\nChecking bucket: {bucket}")
    check_bucket_permissions(bucket)
