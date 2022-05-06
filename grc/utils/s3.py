import io
import base64
import logging
import boto3
#boto3.set_stream_logger('')
from botocore.exceptions import ClientError
from flask import current_app
from botocore.client import Config
from werkzeug.utils import secure_filename


def upload_fileobj(file, object_name):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'], config=Config(signature_version='s3v4'))
    try:
        file.seek(0)
        s3.upload_fileobj(file, current_app.config['BUCKET_NAME'], object_name)  #, ExtraArgs={ 'ACL': 'public-read' })  # Access Denied error

    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return False

    return True


def create_presigned_url(object_name, expiration=36000):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'], config=Config(signature_version='s3v4'))

    try:
        """s3_ = boto3.client(
            's3',
            #aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            #aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION'],
            #endpoint_url='https://s3.' + current_app.config['AWS_REGION'] + '.amazonaws.com',
            #config=Config('s3={'addressing_style': 'virtual'},' signature_version='s3v4')
            config=Config(signature_version='s3v4')
        )

        #data = s3.get_object(Bucket=current_app.config['BUCKET_NAME'], Key=object_name)
        #print('data', flush=True)
        #print(data, flush=True)

        #print('File size', flush=True)
        #print(os.path.getsize('./' + object_name), flush=True)

        print('Bucket: %s' % current_app.config['BUCKET_NAME'], flush=True)
        print('Key: %s' % object_name, flush=True)
        print('ExpiresIn: %s' % str(expiration), flush=True)"""

        url = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': current_app.config['BUCKET_NAME'], 'Key': object_name}, ExpiresIn=expiration, HttpMethod='GET')

    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return None

    return url


def download_object_data(object_name):
    data = None
    width = 0
    height = 0

    try:
        file_type = ''
        if '.' in object_name:
            file_type = object_name[object_name.rindex('.') + 1:]
        file_type = file_type.lower()
        #return 'data:image/' + file_type + ';base64, ', 0, 0

        if file_type == 'jpeg' or file_type == 'jpg' or file_type == 'png' or file_type == 'tif' or file_type == 'bmp':
            byte_value = download_object(object_name)
            if byte_value is not None:
                from PIL import Image
                img = Image.open(byte_value)
                width, height = img.size

                byte_value = byte_value.getvalue()

                if file_type == 'tif' or file_type == 'bmp':
                    jpg = io.BytesIO()
                    img.save(jpg, 'JPEG', quality=100)
                    byte_value = jpg.getvalue()
                    jpg.close()
                    file_type = 'jpeg'

                byte_base64 = base64.b64encode(byte_value)
                data = byte_base64.decode('utf-8')
                if data:
                    if file_type == 'jpg':
                        file_type == 'jpeg'
                    data = 'data:image/' + file_type + ';base64, ' + data

    except ClientError as e:
        logging.error(e)
        print(e, flush=True)

    return data, width, height


def download_object(object_name):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'], config=Config(signature_version='s3v4'))

    print('Downloading %s' % object_name, flush=True)
    data = None
    try:
        bytes_buffer = io.BytesIO()
        s3.download_fileobj(Bucket=current_app.config['BUCKET_NAME'], Key=object_name, Fileobj=bytes_buffer)
        data = bytes_buffer  #.getvalue()

    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return None

    return data


def delete_object(object_name):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'], config=Config(signature_version='s3v4'))
    try:
        s3.delete_object(Bucket=current_app.config['BUCKET_NAME'], Key=object_name)

    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return False

    return True
