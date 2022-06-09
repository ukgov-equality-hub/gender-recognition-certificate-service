import sys
import os
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config


def parse_cmd(argv, switch, val=None):
    for idx, x in enumerate(argv):
        if x in switch:
            if val:
                if len(argv) > (idx + 1):
                    if not argv[idx + 1].startswith('-'):
                        return argv[idx + 1]
            else:
                return True


def main():
    args = sys.argv[1:]
    aws_access_key_id = parse_cmd(args, ['--aws_access_key_id'], True)
    aws_secret_access_key = parse_cmd(args, ['--aws_secret_access_key'], True)
    aws_region = parse_cmd(args, ['--aws_region'], True)
    bucket_name = parse_cmd(args, ['--bucket_name'], True)
    folder = parse_cmd(args, ['--folder'], True)

    if parse_cmd(args, ['help', '-h', '--help'], False):
        print(
            "Simple utility to upload files to AWS S3 buckets\n\n" \
            "Arguments:\n" \
            "command                     emptybucket or upload\n" \
            "--aws_access_key_id\n" \
            "--aws_secret_access_key\n" \
            "--aws_region                AWS region name e.g. eu-west-2\n" \
            "--bucket_name               Name fo the ASW bucket\n\n" \
            "To upload files, an additional folder argument is required:\n" \
            "--folder                    Source folder containing files to upload\n\n" \
            "Example: ./aws.py upload --aws_access_key_id 12345 --aws_secret_access_key 67890 --aws_region eu-west-2 --bucket_name my-bucket --folder /Users/<username>/Downloads/myfolder" \
        )

    else:
        if aws_access_key_id is None:
            print("aws_access_key_id not specified")
            return
        elif aws_secret_access_key is None:
            print("aws_secret_access_key not specified")
            return
        elif aws_region is None:
            print("aws_region not specified")
            return
        elif bucket_name is None:
            print("bucket_name not specified")
            return


        if parse_cmd(args, ['emptybucket'], False):
            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=aws_region,
                    config=Config(signature_version='s3v4')
                )

                for key in s3.list_objects(Bucket=bucket_name)['Contents']:
                    print(f"Deleting {key['Key']}")
                    s3.delete_object(Bucket=bucket_name, Key=key['Key'])

            except Exception as e:
                print(e, flush=True)

        elif parse_cmd(args, ['upload'], False):
            if folder is None:
                print("folder not specified")
                return
            elif not (Path(folder).exists() and Path(folder).is_dir()):
                print("folder not found")
                return

            def upload_fileobj(file, object_name):
                try:
                    s3.upload_file(file, bucket_name, object_name)

                except ClientError as e:
                    print(e)
                    return False

                return True

            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=aws_region,
                    config=Config(signature_version='s3v4')
                )

                for path, subdirs, files in os.walk(folder):
                    for file in files:
                        filename = os.fsdecode(file)
                        print(f"Uploading {filename}")
                        upload_fileobj(os.path.join(path, file), os.fsdecode(file))

            except Exception as e:
                print(e, flush=True)

        else:
            print("Unknown command")


if __name__ == '__main__':
   main()
