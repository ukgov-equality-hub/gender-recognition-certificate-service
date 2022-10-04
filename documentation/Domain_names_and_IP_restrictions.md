
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Domain names and IP restrictions

# Domain names and IP restrictions

## How do I change the IP restrictions?

* Go to the [GitHub Actions Secrets page for this repo](https://github.com/cabinetoffice/grc-app/settings/secrets/actions).  
  Note: you need to have Admin permissions on the repo to access that page

* Edit the `ALLOWED_IPS_ADMIN_[ENVIRONMENT]` secret:
  * [Direct link to ALLOWED_IPS_ADMIN_SANDBOX](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/ALLOWED_IPS_ADMIN_SANDBOX)
  * [Direct link to ALLOWED_IPS_ADMIN_STAGING](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/ALLOWED_IPS_ADMIN_STAGING)
  * [Direct link to ALLOWED_IPS_ADMIN_PRODUCTION](https://github.com/cabinetoffice/grc-app/settings/secrets/actions/ALLOWED_IPS_ADMIN_PRODUCTION)

* Enter the IP addresses you want to allow.  
  **Note:** This must be in Nginx config file format.  
  e.g.  
  ```
  allow 12.34.56.78/32;
  allow 98.76.54.0/24;
  ```  
  Remember:
  * Start each line with `allow`
  * Put the IP range in the middle using `aa.bb.cc.dd/ee` format (IP subnet format)
  * End each line with `;`

* Re-deploy the apps to the environment you want.  
  See [Deployments](Deployments.md) for details.  
  In summary:
  * Pushing to the `master` **branch** deploys to the `sandbox` environment  
  * Pushing a **tag** named `stage-*` deploys to the `staging` environment  
  * Pushing a **tag** named `v*` deploys to the `production` environment  


## How do I set up Domain Name and IP restrictions for a new environment?

Here's how we set up domain names and IP restrictions in PaaS.  
This is based on:
* [Instructions about custom domains from Gov.UK PaaS](https://docs.cloud.service.gov.uk/deploying_services/use_a_custom_domain/)
* [Instructions about route services from Gov.UK PaaS](https://docs.cloud.service.gov.uk/deploying_services/route_services/)
* [GOV.UK PaaS IP authentication route service](https://github.com/alphagov/paas-ip-authentication-route-service)
* [The Gender Pay Gap service's IP deny service](https://github.com/cabinetoffice/gender-pay-gap/tree/main/Infrastructure/gpg-ipdeny)

### Login to Gov.UK PaaS

* Open a Bash terminal in the `hosting` folder

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the GRC organisation and the *sandbox* space:

* Target the space containing the app you want to add domain  
  e.g. one of:
  ```
  cf target -s "sandbox"
  cf target -s "staging"
  cf target -s "production"
  ```

### Create the domain name / cdn-route

* Create a domain name for each application.  
  `cf create-domain geo-gender-recognition-certificate DOMAIN_NAME`  
  You will need to do this separately for each domain/sub-domain you want to use.  
  e.g. to add domains to the apps in the  `staging` environment, you would run:  
  ```shell
  cf create-domain geo-gender-recognition-certificate staging.apply-gender-recognition-certificate.service.gov.uk
  cf create-domain geo-gender-recognition-certificate admin.staging.apply-gender-recognition-certificate.service.gov.uk
  ```  

* Create an instance of the `cdn-route` service for each application.  
  `cf create-service cdn-route cdn-route SERVICE_INSTANCE -c '{"domain": "SUBDOMAIN_LIST"}'`  
  e.g. for the admin app in the `staging` environment, run:  
  ```shell
  cf create-service cdn-route cdn-route grc-staging-cdnroute-admin \
  -c '{"domain": "admin.staging.apply-gender-recognition-certificate.service.gov.uk"}'
  ```

* Add / update DNS records to point the domain name at the cdn-route.  
  * Run the command:  
    `cf service SERVICE_INSTANCE`  
    e.g.
    ```shell
    cf service grc-staging-cdnroute-admin
    ```
    
  * This will produce output like this...  
    ```
    status:    Create in progress
    message:   Provisioning in progress.
    
    Create the following CNAME records to direct traffic from your domains to your CDN route
    admin.staging.apply-gender-recognition-certificate.service.gov.uk => abcdefghijkl.cloudfront.net
    
    To validate ownership of the domain, set the following DNS records
    For domain www.example.com, set DNS record
    
        Name:  _1234567890abcdefghijkl.admin.staging.apply-gender-recognition-certificate.service.gov.uk.
        Type:  CNAME
        Value: _1234567890abcdefghijkl.abcdefghijkl.acm-validations.aws.
        TTL:   86400
    
        Current validation status of www.example.com: PENDING_VALIDATION
    
    started:   2020-06-05T09:28:34Z
    updated:   2020-06-05T09:29:44Z
    ```

  * Set the DNS records it mentions.  
    In this case:  
    ```
    CNAME
    from: admin.staging.apply-gender-recognition-certificate.service.gov.uk
    to: abcdefghijkl.cloudfront.net
    
    CNAME
    from: _1234567890abcdefghijkl.admin.staging.apply-gender-recognition-certificate.service.gov.uk
    to: _1234567890abcdefghijkl.abcdefghijkl.acm-validations.aws
    ```
    
  * Re-run the `cf service SERVICE_INSTANCE` command until it says  
    ```
    ...
    status:    Create succeeded
    ...
    ```

  * **IMPORTANT:** Update the `cdn-route` to allow `Authorization` headers.  
    Run the command:  
    `cf update-service my-cdn-route -c '{"headers": ["Accept", "Authorization"]}'`  
    e.g. for the admin staging route, this would be:  
    ```shell
    cf update-service grc-staging-cdnroute-admin \
    -c '{"headers": ["Accept", "Authorization"]}'
    ```
  
  * Map the route to the app.  
    `cf map-route APP_NAME DOMAIN_NAME`  
    e.g. for the admin staging app, this would be:  
    ```shell
    cf map-route grc-staging-admin \
    admin.staging.apply-gender-recognition-certificate.service.gov.uk
    ```

### Create the IP restrictions app/service

**Note:** We currently only have IP restrictions on the Admin app.

* Create the IP Restrictions app.  
  `cf create-app IP_RESTRICTIONS_APP_NAME`  
  e.g. for admin staging this would be:  
  ```shell
  cf create-app grc-staging-iprestrict-admin
  ```

* Create the user-provided service.  
  `cf create-user-provided-service ROUTE_SERVICE_NAME -r "https://ROUTE_SERVICE_DOMAIN"`  
  e.g. for admin staging this would be:  
  ```shell
  cf create-user-provided-service \
  grc-staging-routeservice-iprestrict-admin \
  -r "https://grc-staging-iprestrict-admin.london.cloudapps.digital"
  ```

* Bind the Route Service to the Domain Name(s)  
  `cf bind-route-service "${APPS_DOMAIN}" "${ROUTE_SERVICE_NAME}" --hostname "${PROTECTED_APP_HOSTNAME}"`  
  &nbsp;  
  **Note:** we need to do this for each domain name (e.g. the PaaS domain and the .gov.uk domain)  
  e.g. for admin staging this would be:  
  ```shell
  # For the .london.cloudapps.digital domain name:
  cf bind-route-service \
  "london.cloudapps.digital" \
  "grc-staging-routeservice-iprestrict-admin" \
  --hostname "grc-staging-admin"
  
  # Then, for the .gov.uk domain name:
  cf bind-route-service \
  "admin.staging.apply-gender-recognition-certificate.service.gov.uk" \
  "grc-staging-routeservice-iprestrict-admin"
  ```

* Push the IP Restrictions app.  
  This should automatically be pushed each time you deploy the app via GitHub.


### Dashboard app
The dashboard app implements IP whitelisting through Flask instead of NGINX, this allows the whitelist to be updated quickly without the need to redeploy the whole app. The IP whitelist is stored as an environment variable within an app.

To update the IP whitelist, login to Cloud Foundry and target your preferred space (production, staging etc) - See *Login to Gov.UK PaaS* above.

* Find the current IP whitelist  
  `cf env APP_NAME` 

* Look for the contents of the environment variable `IP_WHITELIST`

* Update the environment variable by appending your desired IP address to the list, for example, if `IP_WHITELIST` is currently  
  `1.1.1.1`  
  set the new value to (note the comma)  
  `1.1.1.1,2.2.2.2`

* Update the environment variable in Cloud Foundry  
  `cf set-env APP_NAME IP_WHITELIST "1.1.1.1,2.2.2.2"`

* Restart the app  
  `cf restage APP_NAME`
