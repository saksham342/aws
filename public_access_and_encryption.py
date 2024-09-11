import boto3
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
def check_public_access(bucket_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_bucket_acl(Bucket=bucket_name)
        acl = response['Grants']
        for grant in acl:
            if grant['Grantee'].get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                if grant['Permission'] in ['READ', 'FULL_CONTROL']:
                    print(f'Bucket {bucket_name} is publicly accessible.')
                    return True
    except Exception as e:
        print(f'Error checking bucket ACL: {e}')
    return False

def check_encryption(bucket_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_bucket_encryption(Bucket=bucket_name)
        encryption = response['ServerSideEncryptionConfiguration']
        print(f'Bucket {bucket_name} has encryption enabled: {encryption}')
    except s3_client.exceptions.ClientError as e:
        if 'ServerSideEncryptionConfigurationNotFoundError' in str(e):
            print(f'Bucket {bucket_name} does not have encryption enabled.')
        else:
            print(f'Error checking bucket encryption: {e}')

for bucket_name in common_bucket_names:
    print(f"\nChecking bucket: {bucket_name}")
    check_public_access(bucket_name)
    check_encryption(bucket_name)
