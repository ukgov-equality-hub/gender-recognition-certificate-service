
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Deployments

# External backups

Our application is hosted on [Gov.UK Platform as a Service (PaaS)](https://www.cloud.service.gov.uk/).  
We back up our database (and soon, our S3 files) to an AWS S3 bucket outside of Gov.UK PaaS.


## The reasons we need external backups

Gov.UK PaaS backups are insufficient for our needs:
* Gov.UK PaaS keep database backups for only 7 days.  
  If there was a data loss (e.g. some house-keeping code had a mistake and deleted too much data)
  over the Christmas holidays, we might not notice until all the backups had expired.

* If someone with access to Gov.UK PaaS deletes the database (either by mistake or maliciously),
  this also deletes all the backups (this is, perhaps bizarrely, standard practice for AWS RDS).

* We use AWS S3 to store files.  
  We create the S3 bucket through Gov.Uk PaaS.  
  Gov.UK PaaS does not allow us to enable file version history on the S3 bucket.  
  If a code mistake causes files to be deleted or get corrupted, we don't have a way to restore previous versions of the files.

* Additionally, if someone with access to Gov.UK PaaS deletes the entire S3 bucket, we (until now) had no backups of the files within it.


## Goals of the external backups
* Regularly back up the entire database
* Regularly back up all files stored in S3
* Save the backups somewhere outside of Gov.UK PaaS, so that a user with access to PaaS can't delete the backups
* Ensure the backups can be easily accessed by the team, to allow the services to be quickly restored in the event of an outage
* Ensure the data contained within the backups can't easily be accessed by an attacker (i.e. don't open up a new attack vector)
* Ensure the backups can't be deleted for a fixed amount of time (e.g. 35 days)


## Creating the external backups

We use [GitHub Actions](https://docs.github.com/en/actions) to back up the database.  
Here is the [GitHub Actions pipeline that performs the database backup](https://github.com/cabinetoffice/grc-app/actions/workflows/backup-database-to-external-s3.yml).  
The backups run on a schedule (currently once per hour).

This pipeline:
* Takes a backup of the database using the `conduit` CloudFoundry plugin and the `pg_dump` PostgreSQL tool.  
  [Gov.UK PaaS documentation about Conduit](https://docs.cloud.service.gov.uk/guidance.html#using-the-conduit-plugin)  
  [Conduit documentation about how to use Conduit in conjunction with pg_dump](https://github.com/alphagov/paas-cf-conduit/blob/master/README.md#postgres)

* Encrypts the backup file using the `openssl` tool.  
  [OpenSSL documentation about how to encrypt a file](https://wiki.openssl.org/index.php/Enc)

* Uploads the encrypted file to an external S3 bucket


## Preventing backups from being deleted

The external S3 bucket uses the following settings to help with security / object lifecycle management:
* Restrictive IAM users
* S3 Object Lock
* S3 Lifecycle Policies

The IAM user gives the app the minimum possible access to the S3 bucket.  
The S3 Object Locks makes it impossible to delete backups for 35 days.  
The S3 Lifecycle Policy automatically deletes backups after 40 days.  
Together, this means that we don't need any manual housekeeping scripts to tidy up old backup files (which could be error-prone).

### IAM users

We have created a dedicated IAM user with write-only permissions on the bucket.  
Here's the IAM policy:
```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::uk-gov-gender-recognition-certificate-service-backups/*"
        }
    ]
}
```

We've created an IAM user `gender-recognition-certificate-service-user-write-only` with the above policy

### S3 Object Lock

We have enabled S3 Object Lock on the bucket (in Compliance mode).  
[AWS documentation about S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html)  
[How to Configure S3 Object Lock using the AWS console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-console.html)

We've set a retention period of 35 days.

### S3 Lifecycle Policy

We have created a lifecycle policy to automatically delete objects after a certain period.  
[AWS documentation about S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html)  
[How to set a lifecycle configuration on an S3 bucket via the AWS console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html)

We've set a expiration period of 40 days.


## How to restore a database backup

* Ask someone on the team for read-access to the external S3 bucket.  
  They can create you some AWS credentials to access the bucket.  
  This will either be via the AWS console (website) or via the command-line.

* Find and download the database backup you wish to restore.  
  The backups for each environment are saved in different folders.  
  If you're looking to restore the Live service, look for the `production` folder.  
  Look for the most recent backup (that isn't corrupted).  
  If more than one backup has been created at the exact same time, you can use S3 version history to see both versions of the backup file.

* Decrypt the backup file.  
  Check the `.github/workflows/_backup-database-to-external-s3-shared.yml` file to see how backup files are currently encrypted.  
  At the time of writing, we used this command to **encrypt** files:  
  ```shell
  openssl enc -aes-256-cbc -pbkdf2 -in 'database-backup.sql' -out 'database-backup.sql.encrypted' -pass pass:PASSWORD
  ```
  So, you would use the following command to **decrypt** the file:
  ```shell
  openssl enc -d -aes-256-cbc -pbkdf2 -in 'BACKUP_FILENAME.sql.encrypted' -out 'database-backup.sql' -pass pass:PASSWORD
  ```
  Ask a member of the team for the encryption password.

* The decrypted file will be a plain `.sql` file (generated by the `pg_dump` command).  
  You can connect to a database and run this script on the database to re-create and re-populate the database.  
  The `.sql` file contains both the **schema** and the **data**.

### Notes on restoring the database

* Do you want to restore the **schema** and/or the **data**?  
  The backup file contains both.  
  You can easily edit the `.sql` file to remove the schema if this has already been re-created

* When the app is first run, it will create a "default admin user" (if there are no admin users).  
  If you are having trouble restoring the `admin_user` table, it may be that there is already a row in the table
  which is conflicting with the data being restored. Consider deleting the row that has automatically been added
  and try restoring again.
