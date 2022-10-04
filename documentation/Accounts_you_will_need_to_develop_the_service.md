
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Accounts you will need

# Accounts you will need

You will need access to the following systems to develop the Gender Recognition Certificate service.  
Ask an existing member of the team to add you to all of these.

The code:
* Write access to this GitHub repository  
  Normally granted by adding you to the
  [Gender Recognition Certificate GitHub team](https://github.com/orgs/cabinetoffice/teams/gender-recognition-certification)

Services that the Gender Recognition Certificate service depends on:
* [Gov.UK Notify](https://www.notifications.service.gov.uk/)  
  Here's a link to the [Gender Recognition Certificate service on Gov.UK Notify](https://www.notifications.service.gov.uk/services/36bdb0a3-86e3-423d-b1ce-26fae1ead417)

* [Gov.UK Platform as a Service (PaaS)](https://www.cloud.service.gov.uk/)  
  Here's a link to the [Gender Recognition Certificate organisation on Gov.UK PaaS](https://admin.london.cloud.service.gov.uk/organisations/7f161279-648d-4cf4-99c6-0e8af0454f65)
  that you'll need to be added to

* [Gov.UK Pay](https://www.payments.service.gov.uk/)  
  Here's a link to the [Gender Recognition Certificate service on Gov.UK Pay](https://selfservice.payments.service.gov.uk/service/4a23aa76474848b1b003ebe58321ffac/organisation-details)  
  And here's a link to the [Test account](https://selfservice.payments.service.gov.uk/account/9ce8b0f823524e32b74be275880b13db/dashboard) where you can see transactions in the test environments

* [AWS Console access](https://grc-production.signin.aws.amazon.com/console)  
  The Account ID is `grc-production`  
  Whilst the system stores user uploaded files on a PaaS S3 bucket, we also use an external S3 bucket to store encrypted files off-site.  
  When you're logged in, here's a [direct link to the S3 bucket](https://s3.console.aws.amazon.com/s3/buckets/uk-gov-gender-recognition-certificate-service-backups)

* Emails send in the testing environments are sent to [this Google Group](https://groups.google.com/a/cabinetoffice.gov.uk/d/forum/grc-service-account)  
  Ask a team member to add you.  
  The Google Group is a mailing list. You will be forwarded all emails sent to this group.  
  You might want to add a mailbox rule to your Outlook / Gmail so you're not swamped with emails!

Project tools:
* [Trello](https://trello.com/b/E8b3Jgfl)  
  This is where we track progress of development tickets

* [Equality Hub Slack](https://equalityhub.slack.com)  
  Ask an existing member of the team to add you to all the relevant Slack channels

* [Cross-government Slack](https://ukgovernmentdigital.slack.com) (optional, but useful to communicate with Design System, PaaS teams)  
  This can be useful to ask questions to the Design System and PaaS teams.  
  You need a Cabinet Office laptop (in order to get a Cabinet Office email address) to access this

* [Google Chat](https://mail.google.com/chat)  
  Ask a team member for access to the relevant groups

* [Google Analytics](https://analytics.google.com/)  
  Ask a team member for access. The property you need access to is `317472624`

* This [Google Drive folder](https://drive.google.com/drive/u/3/folders/14BJ-tgEuGbdf1Ak0A1G8nUZxP7LdJDa0)

* [Pingdom](https://www.pingdom.com/)  
  This reports on whether the service is up or down - this is sent to the `#support` Slack channel

* [Splunk](https://www.splunk.com/)  
  This captures console outputs for management reporting

Access to the service itself.  
Ask a team member to set you up with:
* An admin account on the [sandbox admin website](https://geo-gender-recognition-certificate-admin.london.cloudapps.digital/)
* An admin account on the [staging admin website](https://grc-staging-admin.london.cloudapps.digital/)
