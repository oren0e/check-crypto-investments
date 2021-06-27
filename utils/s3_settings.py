import os

import boto3

S3_BUCKET = 'check-crypto-inv'
AWS_ID = os.environ.get('AWS_KEY_ID')
AWS_SECRET = os.environ.get('AWS_SECRET_KEY')

if not AWS_ID and not AWS_SECRET:
    raise RuntimeError("Missing AWS credentials")

session = boto3.Session(
    aws_access_key_id=AWS_ID,
    aws_secret_access_key=AWS_SECRET,
)
