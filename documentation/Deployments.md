
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Deployments

# Deployments

We use [GitHub Actions](https://docs.github.com/en/actions) for our deployments.  
Here are the [GitHub Actions pipelines for the GRC service](https://github.com/cabinetoffice/grc-app/actions).

## When are deployments run?
* Pushing to the `master` **branch** deploys to the `sandbox` environment  
  You can see the [sandbox deployments here](https://github.com/cabinetoffice/grc-app/actions/workflows/deploy-sandbox.yml)

* Pushing a **tag** named `stage-*` deploys to the `staging` environment  
  You can see the [staging deployments here](https://github.com/cabinetoffice/grc-app/actions/workflows/deploy-staging.yml)

* Pushing a **tag** named `v*` deploys to the `production` environment  
  You can see the [production deployments here](https://github.com/cabinetoffice/grc-app/actions/workflows/deploy-prod.yml)


## How to deploy to Gov.UK PaaS manually
Normally, it shouldn't be necessary to deploy to PaaS manually.

But, there might be cases where you want to test something quickly in a PaaS environment.  
To deploy to PaaS, follow these instructions:

* Follow the instructions on the [Hosting and live databases](Hosting_and_live_databases.md) page to connect to the hosting environments

* Open a Bash terminal in the `hosting` folder

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the GRC organisation and the *sandbox* space:

* Return to the root folder:  
  `cd ..`

* Run this command  
  ```shell
  cf target -s sandbox
  cf push geo-gender-recognition-certificate --manifest manifest-sandbox.yml --strategy rolling
  ```

Alternatively, you can login directly to PaaS (Note: All users should have Single Sign On enabled):

`cf login --sso`

Select your desired project and target environment to continue. Once logged in, push the code:

`cf push APP_NAME -f MANIFEST_NAME --strategy rolling`

WHERE: `APP_NAME` is the name of the app to be pushed, e.g. `geo-gender-recognition-certificate` and `MANIFEST_NAME` is your manifest file, e.g. `manifest-sandbox.yml`
