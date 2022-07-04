## Useful comands

This file contains a number of useful CLI commands to help with GRC.

## PaaS

* Login to PaaS:  
  `cf login --sso`

* List apps:  
  `cf apps`

* Push an app:  
  `cf push APP_NAME -f MANIFEST_FILE.yml --strategy rolling`

* View app logs:  
  `cf logs APP_NAME --recent`

* List services:  
  `cf services`

* List routes:  
  `cf routes`

* Environment variables:  
  `cf env APP_NAME`  
  `cf set-env APP_NAME KEY_NAME KEY_VALUE`  
  `cf unset-env APP_NAME KEY_NAME`

* Restart an app:  
  `cf restart APP_NAME`  
  `cf restage APP_NAME`

* Binding services to apps:  
  `cf create-service-key SERVICE_NAME SERVICE_KEY -c '{"allow_external_access": true}'`  
  `cf bind-service APP_NAME SERVICE_NAME -c '{"permissions": "PERMISSION"}'`  
  `cf unbind-service APP_NAME SERVICE_NAME`

* Connect to database using Conduit:  
  `cf install-plugin conduit`  
  `cf conduit DB_SERVICE_NAME -- psql`


## AWS S3

The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) can be used to view files on the S3 bucket.

Once installed, your terminal must be [logged into AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). Open your credentials file and add your aws_secret_key_id and aws_secret_access_key:

* On a Mac, edit the file `~/.aws/credentials`

* On a Windows PC, edit the file `C:\Users\username\.aws\credentials`

Your credentials can be found by loging into the AWS console in a web browser, clicking on the acount drop down menu at the top right of the page and choosing "Security credentials"

Once logged in, you can run a number of AWS commands:

* List all objects in an S3 bucket:  
  `aws s3api list-objects --bucket <BUCKET_ID> [--output text]`

* Delete a single file in S3:  
  `aws s3api delete-object --bucket <BUCKET_ID> --key <FILE_KEY>`

* Delete multiple files on S3:  
  `aws s3api delete-objects --bucket <BUCKET_ID> --delete '{"Objects":[{"Key":"<FILE_KEY>"},...]}'`

* Download a list of all keys into a local file:  
  `aws s3api list-objects --bucket <BUCKET_ID> --query 'Contents[].{Key: Key}' --output text > <FILE_NAME>.txt`


The bucket ID can be obtained from environment variables in cloud foundry in the VCAP_SERVICES section, e.g.

`cf env APP_NAME`

A full list of [AWS CLI commands can be found here](https://docs.aws.amazon.com/cli/latest/reference/)
