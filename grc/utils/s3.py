import io
import sys
import logging
import boto3
boto3.set_stream_logger('')
from botocore.exceptions import ClientError
from flask import current_app
from botocore.client import Config

def upload_fileobj(file, object_name):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'])  #, config=Config(signature_version='s3v4'))
    try:
        return s3.upload_fileobj(file, current_app.config['BUCKET_NAME'], object_name) #, ExtraArgs={ 'ACL': 'public-read' }) Access Denied error
    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return False


def create_presigned_url(object_name, expiration=3600):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'])  #, config=Config(signature_version='s3v4'))

    try:
        url = s3.generate_presigned_url('get_object', Params={
                                                        'Bucket': current_app.config['BUCKET_NAME'],
                                                        'Key': object_name
                                                    }, ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return None

    # The response contains the presigned URL
    return url


def download_object(object_name):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'])  #, config=Config(signature_version='s3v4'))

    print('Downloading', flush=True)
    print(object_name, flush=True)
    data = None
    try:
        #object_name = object_name.replace('/', '__')
        url = create_presigned_url('I15AED34/genderEvidence/Screenshot_2022-01-18_at_11.12.35.png')
        print('presigned_url: %s' % url, flush=True)

        #contents = request.urlopen(url).read()
        #print(contents, flush=True)





        # 403 permissions error...
        #data = s3.get_object(Bucket=current_app.config['BUCKET_NAME'], Key=object_name)
        #data = data['Body'].read()
        #print('data', flush=True)
        #print(data, flush=True)

        '''outfile = io.BytesIO()
        s3.download_fileobj(Bucket=current_app.config['BUCKET_NAME'], Key=object_name, Fileobj=outfile)
        outfile.seek(0)
        print('outfile', flush=True)
        print(outfile, flush=True)
        print(sys.getsizeof(outfile), flush=True)'''

        #for key in s3.list_objects(Bucket=current_app.config['BUCKET_NAME'])['Contents']:
        #    print(key['Key'])



        #my_bucket = s3.Bucket(current_app.config['BUCKET_NAME'])
        #for my_bucket_object in my_bucket.objects.all():
        #    print(my_bucket_object, flush=True)
        '''
        import boto3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('mybucket')

        with open('filename', 'wb') as data:
            bucket.download_fileobj('mykey', data)




        import boto3
        s3 = boto3.client('s3')

        with open('filename', 'rb') as data:
            s3.upload_fileobj(data, 'mybucket', 'mykey')
        '''






        #data = s3.download_file(Bucket=current_app.config['BUCKET_NAME'], Key=object_name, Filename='/Users/alistairknight/Desktop/' + object_name.replace('/', '__'))
    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return None

    # The response
    return data


def delete_object(object_name):
    s3 = boto3.client('s3', region_name=current_app.config['AWS_REGION'])  #, config=Config(signature_version='s3v4'))
    try:
        return s3.delete_object(Bucket=current_app.config['BUCKET_NAME'], Key=object_name)
    except ClientError as e:
        logging.error(e)
        print(e, flush=True)
        return False
