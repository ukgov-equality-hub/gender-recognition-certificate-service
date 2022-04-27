
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
How to put the service into Maintenance Mode

# How to put the service into Maintenance Mode / make the service unavailable

## What is this for?
It may occasionally be necessary to put the application into Maintenance Mode / make the service unavailable.

For example, if we detect a problem, and want to make sure no-one uses the service whilst the service is broken.


## What does Maintenance Mode look like

We use the [Gov.UK Design System "Service unavailable" pattern](https://design-system.service.gov.uk/patterns/service-unavailable-pages/).

All pages on the website will be replaced with a page saying "Sorry, the service is unavailable"


## How to activate / deactivate Maintenance Mode

* Follow the instructions on the [Hosting and live databases](Hosting_and_live_databases.md) page to connect to the hosting environments

* Open a Bash terminal in the `hosting` folder

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the GRC organisation and the *sandbox* space:

* Target the space containing the app you want to put into Maintenance Mode  
  e.g. one of:
  ```
  cf target -s "sandbox"
  cf target -s "staging"
  cf target -s "production"
  ```

* Maintenance Mode is set using an environment variable.  
  You can check the current status of Maintenance Mode using `cf env`  
  e.g. one of:
  ```
  cf env "geo-gender-recognition-certificate"    // Sandbox environment
  cf env "grc-staging"                           // Stanging environment
  cf env "grc-production"                        // Production environment
  ```
  This will print out **all** the environment variables (and there are a lot of them!)
  ```
  Getting env variables for app geo-gender-recognition-certificate in org geo-gender-recognition-certificate / space sandbox as james@jwgsoftware.com...
  ...
  ... about 100 lines later ...
  ...
  MAINTENANCE_MODE: OFF
  ```

* Use `cf set-env` to turn Maintenance Mode on or off  
  e.g. one of:
  ```
  cf set-env "geo-gender-recognition-certificate" MAINTENANCE_MODE ON    // Sandbox environment - ON
  cf set-env "grc-staging" MAINTENANCE_MODE ON                           // Stanging environment - ON
  cf set-env "grc-production" MAINTENANCE_MODE ON                        // Production environment - ON
  
  cf set-env "geo-gender-recognition-certificate" MAINTENANCE_MODE OFF    // Sandbox environment - OFF
  cf set-env "grc-staging" MAINTENANCE_MODE OFF                           // Stanging environment - OFF
  cf set-env "grc-production" MAINTENANCE_MODE OFF                        // Production environment - OFF
  ```

* Restart the app  
  e.g. one of:
  ```
  cf restart "geo-gender-recognition-certificate"    // Sandbox environment
  cf restart "grc-staging"                           // Stanging environment
  cf restart "grc-production"                        // Production environment
  ```
