import boto3
from botocore.config import Config as BotocoreConfig
from botocore import UNSIGNED

# Disable request signing
unsigned_config = BotocoreConfig(signature_version=UNSIGNED)

# List of some S3 bucket names
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

# Create the S3 client with no signing
s3 = boto3.client('s3', config=unsigned_config)


def check_bucket_acl(bucket_name):
    try:
        # Get the bucket ACL
        acl_response = s3.get_bucket_acl(Bucket=bucket_name)
        print("Bucket ACL:")
        for grant in acl_response['Grants']:
            grantee = grant['Grantee']
            grantee_type = grantee.get('Type')
            grantee_uri = grantee.get('URI', 'N/A')
            permission = grant['Permission']
            print(f"Type: {grantee_type}, URI: {grantee_uri}, Permission: {permission}")
    except Exception as e:
        print(f'Error fetching bucket ACL: {e}')

def check_bucket_policy(bucket_name):
    try:
        # Get the bucket policy
        policy_response = s3.get_bucket_policy(Bucket=bucket_name)
        policy = policy_response['Policy']
        print("Bucket Policy:")
        print(policy)
    except Exception as e:
        # AWS returns an error if the bucket policy does not exist or access is denied
        print(f'Error fetching bucket policy: {e}')

# Check bucket ACL and policy
for bucket_name in common_bucket_names:
    print(f"\nDisplaying ACL and Policy for bucket: {bucket_name}")
    check_bucket_acl(bucket_name)
    check_bucket_policy(bucket_name)
