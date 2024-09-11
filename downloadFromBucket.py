import boto3
from botocore.config import Config
from botocore import UNSIGNED
from botocore.client import Config as BotocoreConfig
import os

# Disable request signing
unsigned_config = BotocoreConfig(signature_version=UNSIGNED)

# Create the S3 client with no signing
s3 = boto3.client('s3', config=unsigned_config)

bucket_name = input("Enter your bucket name: ")
download_directory = './downloads'  # Local directory to save downloaded files

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

def download_object(bucket, key, download_dir):
    # Create the full path for the file
    local_path = os.path.join(download_dir, key)
    
    # Create local directories if they don't exist
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # Download the object
    try:
        s3.download_file(bucket, key, local_path)
        print(f"Downloaded: {key} to {local_path}")
    except Exception as e:
        print(f"Failed to download {key}: {e}")

try:
    # List objects in the S3 bucket without signing the request
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    while True:
        # Iterate over each object in the response
        for obj in response.get('Contents', []):
            key = obj['Key']
            download_object(bucket_name, key, download_directory)
        
        # Check if there's more data to be fetched
        if response.get('IsTruncated'):
            # Fetch the next set of objects
            response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=response['NextContinuationToken'])
        else:
            break

except Exception as e:
    print(f'Error: {e}')
