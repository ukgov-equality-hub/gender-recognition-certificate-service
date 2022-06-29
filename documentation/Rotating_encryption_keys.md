
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Rotating encryption keys

# Rotating encryption keys
Here are a list of the secrets / keys / encryption keys that we will want to rotate from time to time (e.g. before we go live):

## Gov.UK Notify

### Generate new Gov.UK Notify keys
[Gov.UK Notify API keys](https://www.notifications.service.gov.uk/services/36bdb0a3-86e3-423d-b1ce-26fae1ead417/api/keys)  

See the [Gov.UK Notify documentation about key types](https://docs.notifications.service.gov.uk/python.html#api-keys)  
We should have:
* 1 [Live key](https://docs.notifications.service.gov.uk/python.html#live).    
  This sends real emails.  
  We will use this on the production app.
* 1 [Team and guest list key](https://docs.notifications.service.gov.uk/python.html#team-and-guest-list).  
  This only sends emails to the team and uo to 5 people on a "guest list".  
  We will use this on the sandbox / staging apps
* 1 [Test key](https://docs.notifications.service.gov.uk/python.html#test).  
  This pretends to send emails.  
  We use this for automated testing.
* We should probably avoid having other keys hanging around, otherwise we'll get confused about which are in use.

### Use the new Gov.UK Notify keys
This needs to be set in 3 places:
* Local development:  
  Edit the `NOTIFY_API` setting in the env files:
  * `.env`
  * `.admin.env`

* In Gov.UK PaaS:  
  Set the `NOTIFY_API` environment variable on all 6 environments.  
  **Note:** Take care to use the right key for each environment!
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate NOTIFY_API "TEAM_AND_GUEST_LIST_KEY"
  cf restart geo-gender-recognition-certificate --strategy rolling
  
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate-admin NOTIFY_API "TEAM_AND_GUEST_LIST_KEY"
  cf restart geo-gender-recognition-certificate-admin --strategy rolling
  
  cf target -s staging
  cf set-env grc-staging NOTIFY_API "TEAM_AND_GUEST_LIST_KEY"
  cf restart grc-staging --strategy rolling
  
  cf target -s staging
  cf set-env grc-staging-admin NOTIFY_API "TEAM_AND_GUEST_LIST_KEY"
  cf restart grc-staging-admin --strategy rolling
  
  cf target -s production
  cf set-env grc-production NOTIFY_API "***LIVE_KEY***"
  cf restart grc-production --strategy rolling
  
  cf target -s production
  cf set-env grc-production-admin NOTIFY_API "***LIVE_KEY***"
  cf restart grc-production-admin --strategy rolling
  ```

* If you are changing the **Test Key**, this is used by our automated tests that run in GitHub  
  We'll need to update the **Test Key** in [GitHub Actions Secrets](https://github.com/cabinetoffice/grc-app/settings/secrets/actions)  
  Here's the [direct link to the TEST_NOTIFY_API secret](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/TEST_NOTIFY_API)
  

## Gov.UK Pay

### Generate new Gov.UK Pay keys
[Gov.UK Pay API keys (live account)](https://selfservice.payments.service.gov.uk/account/11eca0c3b3e54e09ba5bcc8f80dc2b6f/api-keys)  
[Gov.UK Pay API keys (test account)](https://selfservice.payments.service.gov.uk/account/9ce8b0f823524e32b74be275880b13db/api-keys)  

### Use the new Gov.UK Pay keys
This needs to be set in 3 places:
* Local development:  
  Edit the `GOVUK_PAY_API_KEY` setting in the `.env` file

* In Gov.UK PaaS:  
  Set the `GOVUK_PAY_API_KEY` environment variable - **only the main app**, not the admin app.  
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate GOVUK_PAY_API_KEY "TEST_KEY"
  cf restart geo-gender-recognition-certificate --strategy rolling
  
  cf target -s staging
  cf set-env grc-staging GOVUK_PAY_API_KEY "TEST_KEY"
  cf restart grc-staging --strategy rolling
  
  cf target -s production
  cf set-env grc-production GOVUK_PAY_API_KEY "***LIVE_KEY***"
  cf restart grc-production --strategy rolling
  ```

* If you are changing the **Test Key**, this is used by our automated tests that run in GitHub  
  We'll need to update the **Test Key** in [GitHub Actions Secrets](https://github.com/cabinetoffice/grc-app/settings/secrets/actions)  
  Here's the [direct link to the AUTOMATED_TEST_GOVUK_PAY_API_KEY secret](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/AUTOMATED_TEST_GOVUK_PAY_API_KEY)
  

## External Backup AWS Keys
We store backups of our database and S3 files outside of Gov.UK PaaS.  
See the [External backups](External_backups.md) page for details.

This uses a separate AWS account.  
On the AWS account, we have created a user with write-only access to a single S3 bucket.  
We give the user credentials to the app and GitHub to allow them to send backup files to the external S3 bucket.

We might want to re-generate the AWS access key id / AWS secret access key for this user.

### Generate new credentials for the AWS user
* [Login to the AWS console](https://grc-production.signin.aws.amazon.com/console)
* Go to IAM.  
  Find the user `gender-recognition-certificate-service-user-write-only`.  
  Go to the _Security credentials_ tab.  
  Or, follow this [direct link to the Security Credentials tab for this user](https://us-east-1.console.aws.amazon.com/iam/home#/users/gender-recognition-certificate-service-user-write-only?section=security_credentials).
* Click "Create access key"
* Copy the "Access key ID" and "Secret access key"
* Deactivate / delete the old key (once you've set the new key - see below)

### Use new credentials for the AWS user
This needs to be set in 3 places:
* Local development:  
  In the `.admin.env` file, edit the settings:  
  * Set the **Access key ID** in the setting `EXTERNAL_S3_AWS_ACCESS_KEY_ID`  
  * Set the **Secret access key** in the setting `EXTERNAL_S3_AWS_SECRET_ACCESS_KEY`  

* [GitHub Actions Secrets](https://github.com/cabinetoffice/grc-app/settings/secrets/actions)
  * Set the **Access key ID** in the secret `EXTERNAL_S3_AWS_ACCESS_KEY_ID`  
  Here's the [direct link to the EXTERNAL_S3_AWS_ACCESS_KEY_ID secret](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/EXTERNAL_S3_AWS_ACCESS_KEY_ID)  
  * Set the **Secret access key** in the secret `EXTERNAL_S3_AWS_SECRET_ACCESS_KEY`  
  Here's the [direct link to the EXTERNAL_S3_AWS_SECRET_ACCESS_KEY secret](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/EXTERNAL_S3_AWS_SECRET_ACCESS_KEY)  

* In Gov.UK PaaS:  
  Set 2 environment variables - **only the admin app**, not the public-facing app.  
  The environment variables are:
  * Set the **Access key ID** in the variables `EXTERNAL_S3_AWS_ACCESS_KEY_ID`  
  * Set the **Secret access key** in the variables `EXTERNAL_S3_AWS_SECRET_ACCESS_KEY`  
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate-admin EXTERNAL_S3_AWS_ACCESS_KEY_ID "NEW_ACCESS_KEY_ID"
  cf set-env geo-gender-recognition-certificate-admin EXTERNAL_S3_AWS_SECRET_ACCESS_KEY "NEW_SECRET_ACCESS_KEY"
  cf restart geo-gender-recognition-certificate-admin --strategy rolling
  
  cf target -s staging
  cf set-env grc-staging-admin EXTERNAL_S3_AWS_ACCESS_KEY_ID "NEW_ACCESS_KEY_ID"
  cf set-env grc-staging-admin EXTERNAL_S3_AWS_SECRET_ACCESS_KEY "NEW_SECRET_ACCESS_KEY"
  cf restart grc-staging-admin --strategy rolling
  
  cf target -s production
  cf set-env grc-production-admin EXTERNAL_S3_AWS_ACCESS_KEY_ID "NEW_ACCESS_KEY_ID"
  cf set-env grc-production-admin EXTERNAL_S3_AWS_SECRET_ACCESS_KEY "NEW_SECRET_ACCESS_KEY"
  cf restart grc-production-admin --strategy rolling
  ```


## External Backup Encryption Key
This is an encryption key used for our external-to-PaaS backups of the database and files.

### Generate new External Backup Encryption Key
See [How to generate keys](#How-to-generate-keys) at the bottom of this page

### Use new External Backup Encryption Key
This needs to be set in 2 places:
* [GitHub Actions Secrets](https://github.com/cabinetoffice/grc-app/settings/secrets/actions)  
  Here's the [direct link to the EXTERNAL_BACKUP_ENCRYPTION_KEY secret](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/EXTERNAL_BACKUP_ENCRYPTION_KEY)

* In Gov.UK PaaS:  
  Set the `EXTERNAL_BACKUP_ENCRYPTION_KEY` environment variable - **only the admin app**, not the public-facing app.  
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate-admin EXTERNAL_BACKUP_ENCRYPTION_KEY "NEW_ENCRYPTION_KEY"
  cf restart geo-gender-recognition-certificate-admin --strategy rolling
  
  cf target -s staging
  cf set-env grc-staging-admin EXTERNAL_BACKUP_ENCRYPTION_KEY "NEW_ENCRYPTION_KEY"
  cf restart grc-staging-admin --strategy rolling
  
  cf target -s production
  cf set-env grc-production-admin EXTERNAL_BACKUP_ENCRYPTION_KEY "NEW_ENCRYPTION_KEY"
  cf restart grc-production-admin --strategy rolling
  ```


## Job Token

### Generate new Job Token
See [How to generate keys](#How-to-generate-keys) at the bottom of this page

### Use new Job Token
This needs to be set in 2 places:
* [GitHub Actions Secrets](https://github.com/cabinetoffice/grc-app/settings/secrets/actions)  
  Here's the [direct link to the JOB_TOKEN secret](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/JOB_TOKEN)

* In Gov.UK PaaS:  
  Set the `JOB_TOKEN` environment variable - **only the admin app**, not the public-facing app.  
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate-admin JOB_TOKEN "NEW_JOB_TOKEN"
  cf restart geo-gender-recognition-certificate-admin --strategy rolling
  
  cf target -s staging
  cf set-env grc-staging-admin JOB_TOKEN "NEW_JOB_TOKEN"
  cf restart grc-staging-admin --strategy rolling
  
  cf target -s production
  cf set-env grc-production-admin JOB_TOKEN "NEW_JOB_TOKEN"
  cf restart grc-production-admin --strategy rolling
  ```


## Secret Key
The SECRET_KEY is used by Flask to encrypt the session cookie sent to the user.

### Generate new Secret Key
**Note:** Generate a **different key for each environment**.  
See [How to generate keys](#How-to-generate-keys) at the bottom of this page.  

### Use new Secret Key
There are 4 places this can be updated:  
**Remember:** We need a **different key for each environment** (including local development).

* Local development:  
  Edit the `SECRET_KEY` setting in the env files:
  * `.env`
  * `.admin.env`

* In Gov.UK PaaS (sandbox):  
  Set the `SECRET_KEY` environment variable - **in both the main and admin apps**.  
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate SECRET_KEY "NEW_SECRET_KEY__SANDBOX"
  cf restart geo-gender-recognition-certificate --strategy rolling
  
  cf set-env geo-gender-recognition-certificate-admin SECRET_KEY "NEW_SECRET_KEY__SANDBOX"
  cf restart geo-gender-recognition-certificate-admin --strategy rolling
  ```

* In Gov.UK PaaS (staging):  
  Set the `SECRET_KEY` environment variable - **in both the main and admin apps**.  
  ```shell
  cf target -s staging
  cf set-env grc-staging SECRET_KEY "NEW_SECRET_KEY__STAGING"
  cf restart grc-staging --strategy rolling
  
  cf set-env grc-staging-admin SECRET_KEY "NEW_SECRET_KEY__STAGING"
  cf restart grc-staging-admin --strategy rolling
  ```

* In Gov.UK PaaS (production):  
  Set the `SECRET_KEY` environment variable - **in both the main and admin apps**.  
  ```shell
  cf target -s production
  cf set-env grc-production SECRET_KEY "NEW_SECRET_KEY__PROD"
  cf restart grc-production --strategy rolling
  
  cf set-env grc-production-admin SECRET_KEY "NEW_SECRET_KEY__PROD"
  cf restart grc-production-admin --strategy rolling
  ```


## SqlAlchemy Key
The SQLALCHEMY_KEY is used by SqlAlchemy to encrypt cells in the database.

**WARNING:** If you change this, **EXISTING DATA IN THE DATABASE WILL BECOME UNREADABLE**.  

You should only change this if:
* The database is empty, or
* You have worked out a migration plan for decrypting/re-encrypting the data

### Generate new SqlAlchemy Key
**Note:** Generate a **different key for each environment**.  
See [How to generate keys](#How-to-generate-keys) at the bottom of this page.  

### Use new SqlAlchemy Key
There are 4 places this can be updated:  
**Remember:** We need a **different key for each environment** (including local development).

* Local development:  
  Edit the `SQLALCHEMY_KEY` setting in the env files:
  * `.env`
  * `.admin.env`

* In Gov.UK PaaS (sandbox):  
  Set the `SQLALCHEMY_KEY` environment variable - **in both the main and admin apps**.  
  ```shell
  cf target -s sandbox
  cf set-env geo-gender-recognition-certificate SQLALCHEMY_KEY "NEW_SQLALCHEMY_KEY__SANDBOX"
  cf restart geo-gender-recognition-certificate --strategy rolling
  
  cf set-env geo-gender-recognition-certificate-admin SQLALCHEMY_KEY "NEW_SQLALCHEMY_KEY__SANDBOX"
  cf restart geo-gender-recognition-certificate-admin --strategy rolling
  ```

* In Gov.UK PaaS (staging):  
  Set the `SQLALCHEMY_KEY` environment variable - **in both the main and admin apps**.  
  ```shell
  cf target -s staging
  cf set-env grc-staging SQLALCHEMY_KEY "NEW_SQLALCHEMY_KEY__STAGING"
  cf restart grc-staging --strategy rolling
  
  cf set-env grc-staging-admin SQLALCHEMY_KEY "NEW_SQLALCHEMY_KEY__STAGING"
  cf restart grc-staging-admin --strategy rolling
  ```

* In Gov.UK PaaS (production):  
  Set the `SQLALCHEMY_KEY` environment variable - **in both the main and admin apps**.  
  ```shell
  cf target -s production
  cf set-env grc-production SQLALCHEMY_KEY "NEW_SQLALCHEMY_KEY__PROD"
  cf restart grc-production --strategy rolling
  
  cf set-env grc-production-admin SQLALCHEMY_KEY "NEW_SQLALCHEMY_KEY__PROD"
  cf restart grc-production-admin --strategy rolling
  ```


## CF_USERNAME and CF_PASSWORD ?

**TODO**




## How to generate keys
A few options for generating keys:
* Use a password manager's "Generate new password" feature  
  Here's an [online password generator from password manager 1Password](https://1password.com/password-generator/)
* Use [Random.org's password generator](https://www.random.org/passwords/?num=5&len=20&format=html&rnd=new)  
  You probably want to concatenate a few of these together
* The python script below:  
  **Note:** This prints the password in hex `[0-9a-f]`.  
  This has less entropy per characters than a password generator which will use characters `[0-9a-zA-Z]`.  
  So, you'll need a correspondingly longer password to achieve the same security.  
  ```shell
  python -c 'import secrets; print(secrets.token_urlsafe(48))'
  ```
