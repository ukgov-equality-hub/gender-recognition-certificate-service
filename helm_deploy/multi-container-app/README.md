# Multi Container Ruby App Helm Chart
## Introduction
This directory contains the necessary files required to install the MoJ Multi Container Ruby application via the Helm package manager. This application is intended to be used to demonstrate the ease of deployment on a MoJ Cloud Platform. 

The default installation include all components (API server, postgres, worker, rails app) of this application. The postgresql database runs in a ephemeral docker container. When deploying to [cloud platform][cloudplatform], this can be  disabled and setup a RDS instance using the [terraform module] (https://github.com/ministryofjustice/cloud-platform-terraform-rds-instance).

## Installing the Chart
To install the chart:

Update the `values.yaml` file for `databaseUrlSecretName` with the name of the secret where the postgresql URL is stored and `ingress.hosts.host` for the url of the app.

Check (user guide)[https://user-guide.cloud-platform.service.justice.gov.uk/documentation/deploying-an-app/add-secrets-to-deployment.html#adding-a-secret-to-an-application] for how to create kubernetes secret.

```
helm install  multi-container-demo . --values values.yaml --namespace <namespace-name> 
```

The ```namespace-name``` here is the environment name (namespace) you've created in the [Creating a Cloud Platform Environment](https://ministryofjustice.github.io/cloud-platform-user-docs/cloud-platform/env-create/#creating-a-cloud-platform-environment) guide.


There are a number of install switches available. Please visit the [Helm docs](https://docs.helm.sh/helm/#helm-install) for more information. 

The chart has a dependency for postgres, that can be seen in the chart's requirements file: `requirements.yaml`

## Deleting the Chart
To delete the installation from your cluster:
```
helm delete multi-container-demo --namespace <namespace-name> 
```
## Configuration
### Parent chart - multi-container-app

| Parameter  | Description     | Default |
| ---------- | --------------- | ------- |
| `databaseUrlSecretName` | Secret name where the database url is stored with the key `url` | REQUIRED |
| `contentapiurl` | Service url of content-api component | http://content-api-service:4567/image_url.json |
| `ingress.enabled` | Ingress for rails-app | true |
| `ingress.hosts.host` | Ingress url for the app | REQUIRED |
| `postgresql.enabled` | Install Postgres database in a container  | true |
| `postgresql.existingSecret` | Name of existing kubernetes secret to use for PostgreSQL passwords | container-postgres-secrets |
| `posgresql.postgresqlDatabase` | Name of PostgreSQL database | multi_container_demo_app |
| `postgresql.persistence.enabled` | Enable persistence using PVC | false |
| `contentapi.replicaCount` | Number of replica pods used. | 1 |
| `contentapi.image.repository` | The image repository location. | `ministryofjustice/cloud-platform-multi-container-demo-app`|
| `contentapi.image.tag` | The image tag. | `worker-1.4` |
| `contentapi.image.pullPolicy` | Whether the image should pull | `IfNotPresent` |
| `contentapi.containetPort` | Container port to be used by the service  | `Always` |
| `contentapi.service.type` | The type of service you wish to use | `ClusterIP` |
| `contentapi.service.port` | The port your service will use | `4567` |
| `contentapi.service.targetPort` | The container port service will target for | `4567` |
| `railsapp.replicaCount` | Used to set the number of replica pods used. | `1` |
| `railsapp.image.repository` | The image repository location. | `ministryofjustice/cloud-platform-multi-container-demo-app`|
| `railsapp.image.tag` | The image tag. | `rails-app-1.4` |
| `railsapp.image.pullPolicy` | Whether the image should pull | `IfNotPresent` |
| `railsapp.containerPort` | Container port to be used by the service  | `3000` |
| `railsapp.service.type` | The type of service you wish to use | `ClusterIP` |
| `railsapp.service.port` | The port your service will use | `"3000"` |
| `railsapp.service.targetPort` | The container port service will target for | `"3000"` |
| `worker.replicaCount` | Used to set the number of replica pods used. | `1` |
| `worker.image.repository` | The image repository location. | `ministryofjustice/cloud-platform-multi-container-demo-app`|
| `worker.image.tag` | The image tag. | `worker-1.4` |
| `worker.image.pullPolicy` | Whether the image should pull | `IfNotPresent` |
| `worker.containetPort` | Container port to be used by the service  | `Always` |

## Chart Structure
### Chart.yaml
The YAML for our chart. This contains our API version, chart description, name and version. 

### values.yaml
The default configuration values for this chart.

### requirements.yaml
The dependencies to install this chart.

### charts/
A directory containing all subcharts upon which this chart depends.


## Deleting the Chart
To delete the installation from your cluster:
```
helm delete multi-container-demo --namespace <namespace-name> 
```

## Secrets
Change the `container-postgres-secrets.yaml` file to set the password for admin user `postgres`. Refer parameters section of [postgres helm chart](https://github.com/helm/charts/tree/master/stable/postgresql) 

