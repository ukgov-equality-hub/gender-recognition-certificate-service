import io
import base64
import logging
import boto3
from botocore.exceptions import ClientError
from flask import current_app
from botocore.client import Config
from grc.utils.config_helper import ConfigHelper


class AwsS3Client:
    def __init__(self):
        if ConfigHelper.get_vcap_services() is not None:
            creds = ConfigHelper.get_vcap_services().aws_s3_bucket[0].credentials
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=creds.aws_access_key_id,
                aws_secret_access_key=creds.aws_secret_access_key,
                region_name=creds.aws_region,
                config=Config(signature_version='s3v4')
            )
            self.bucket_name = creds.bucket_name

        else:
            self.s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'], config=Config(signature_version='s3v4'))
            self.bucket_name = current_app.config['BUCKET_NAME']


    def upload_fileobj(self, file, object_name):
        try:
            file.seek(0)
            self.s3.upload_fileobj(file, self.bucket_name, object_name)

        except ClientError as e:
            logging.error(e)
            print(e, flush=True)
            return False

        return True


    def download_object_data(self, object_name):
        data = None
        width = 0
        height = 0

        try:
            file_type = ''
            if '.' in object_name:
                file_type = object_name[object_name.rindex('.') + 1:]
            file_type = file_type.lower()

            if file_type == 'jpeg' or file_type == 'jpg' or file_type == 'png' or file_type == 'tif' or file_type == 'bmp':
                byte_value = self.download_object(object_name)
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
                            file_type = 'jpeg'
                        data = 'data:image/' + file_type + ';base64, ' + data

        except ClientError as e:
            logging.error(e)
            print(e, flush=True)

        return data, width, height


    def download_object(self, object_name):
        print('Downloading %s' % object_name, flush=True)
        data = None
        try:
            bytes_buffer = io.BytesIO()
            self.s3.download_fileobj(Bucket=self.bucket_name, Key=object_name, Fileobj=bytes_buffer)
            data = bytes_buffer  #.getvalue()

        except ClientError as e:
            logging.error(e)
            print(e, flush=True)
            return None

        return data


    def delete_object(self, object_name):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)

        except ClientError as e:
            logging.error(e)
            print(e, flush=True)
            return False

        return True
