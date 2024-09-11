import boto3
from botocore.exceptions import ClientError
import threading

# List of bucket names to check
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

# Create the S3 client
s3 = boto3.client('s3')

def get_cors_policy(bucket_name):
    """Retrieve and print the CORS policy for a bucket."""
    try:
        response = s3.get_bucket_cors(Bucket=bucket_name)
        cors_rules = response.get('CORSRules', [])
        
        if cors_rules:
            print(f"\nBucket: {bucket_name}")
            print("CORS Policy:")
            for rule in cors_rules:
                print(f"  Allowed Methods: {rule.get('AllowedMethods', [])}")
                print(f"  Allowed Origins: {rule.get('AllowedOrigins', [])}")
                print(f"  Allowed Headers: {rule.get('AllowedHeaders', [])}")
                print(f"  Expose Headers: {rule.get('ExposeHeaders', [])}")
                print(f"  Max Age Seconds: {rule.get('MaxAgeSeconds', '')}")
        else:
            print(f"\nBucket: {bucket_name}")
            print("CORS Policy: No CORS policy configured.")
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            print(f"\nBucket: {bucket_name}")
            print("Error: Bucket does not exist.")
        elif error_code == 'NoSuchCORSConfiguration':
            print(f"\nBucket: {bucket_name}")
            print("Error: No CORS configuration found.")
        else:
            print(f"\nBucket: {bucket_name}")
            print(f"Error: {e}")

# Iterate over the list of common bucket names
for bucket in common_bucket_names:
    threading.Thread(target=get_cors_policy, args=(bucket,)).start()
    # get_cors_policy(bucket)
