import logging
import boto3
from botocore.exceptions import ClientError
from flask import current_app
from botocore.client import Config

def upload_fileobj(file, object_name):
    """Upload a file to an S3 bucket

    :param file: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Upload the file
    s3 = boto3.client('s3')
    try:
        return s3.upload_fileobj(file, current_app.config['BUCKET_NAME'], object_name)
    except ClientError as e:
        logging.error(e)
        return False


def create_presigned_url(object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3 = boto3.client('s3',region_name=current_app.config['AWS_REGION'], config=Config(signature_version='s3v4'))
    try:
        url = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': current_app.config['BUCKET_NAME'],
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        print(e)
        return None

    # The response contains the presigned URL
    return url