
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Hosting and live databases

# Hosting and live databases

Our code is hosted on [Gov.UK Platform as a Service (Gov.UK PaaS)](https://www.cloud.service.gov.uk/).  
See this link for the [GRC organisation on Gov.Uk PaaS](https://admin.london.cloud.service.gov.uk/organisations/7f161279-648d-4cf4-99c6-0e8af0454f65).

## Connect to Gov.UK PaaS using the CloudFoundry CLI
You will need to connect to the hosting environments to do things like:
* make changes to the environments (e.g. change the scaling of the servers)
* to access databases

For regular deployments, you won't need to connect to Gov.UK PaaS directly.  
Instead, you should use our CI/CD server, GitHub Actions.  
See the [Deployments](Deployments.md) page for details.

Follow these instructions to connect to Gov.UK PaaS:
* First, ask a team member for access to the [GRC organisation on Gov.Uk PaaS](https://admin.london.cloud.service.gov.uk/organisations/7f161279-648d-4cf4-99c6-0e8af0454f65).

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the GRC organisation and the *sandbox* space:  
  ```
  $ ./LoginToGovPaas.sh
  API endpoint: api.london.cloud.service.gov.uk
  Authenticating...
  OK
  Targeted org geo-gender-recognition-certificate.
  Targeted space sandbox.
  API endpoint:   https://api.london.cloud.service.gov.uk
  API version:    3.115.0
  user:           [your email address]
  org:            geo-gender-recognition-certificate
  space:          sandbox
  ```

## Change which space you are targetting within CloudFoundry
Each environment has its own *space* in CloudFoundry.  
We use `cf target` to change space  
e.g.:

```
cf target -s "sandbox"
cf target -s "staging"
cf target -s "production"
```

## Connect to databases hosted on Gov.UK PaaS

* Install the `conduit` CloudFoundry plugin  
  `cf install-plugin conduit`

* Run the relevant `./ConnectToPaas_DB_*.sh` script (e.g. `./ConnectToPaas_DB_Sandbox.sh`)  
  This will:
  * Log you in to Gov.UK PaaS (using the `LoginToGovPaaS.sh` script mentioned above)
  * Fetch the database details (username and password)
  * Make a VPN-like connection to the relevant PaaS database

  The output looks like this (I've replaced irrelevant bits with `...` for simplicity):
  ```
  $ ./ConnectToPaas_DB_Sandbox.sh
  API endpoint: api.london.cloud.service.gov.uk
  
  Authenticating...
  ...
  ...
  ...
  =======================================
  HERE ARE THE KEYS YOU MIGHT WANT TO USE
  =======================================
  
  Host: 127.0.0.1
  Port: 7100
  Username & Password: see below
  
  Getting key postgres-13-dev-developerkey for service instance postgres-13-dev as james@jwgsoftware.com...
  {
   "host": "...",
   "jdbcuri": "...",
   "name": "...",
   "password": "PASSWORD_THAT_YOU_SHOULD_USE",
   "port": ...,
   "uri": "...",
   "username": "USERNAME_THAT_YOU_SHOULD_USE"
  }
  
  ===========================
  IGNORE KEYS PAST THIS POINT
  ===========================  
  ...
  ...
  ...
  ...
  ...
  Press Ctrl+C to shutdown.
  ```

* Use your database UI (e.g. pgAdmin, DataGrip, etc.) to connect to the database using the details above)  
  For ease, here they are for each environment:
  * **Sandbox:**  
    Host: `localhost` or `127.0.0.1`  
    Port: `7100`  
    Username and password: see the output from the command you ran as above
  * **Staging:**  
    Host: `localhost` or `127.0.0.1`  
    Port: `7200`  
    Username and password: see the output from the command you ran as above
  * **Production:**  
    Host: `localhost` or `127.0.0.1`  
    Port: `7300`  
    Username and password: see the output from the command you ran as above  
    **Note:** it's very rare we'd want to connect to production, given the sensitivity of the information.  
    This will mainly be used when setting up the production database, before the service goes live.



