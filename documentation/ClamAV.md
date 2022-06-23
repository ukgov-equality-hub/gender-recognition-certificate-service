
[Gender Recognition Certificate service](../README.md) >
[Developer documentation](README.md) >
Clam AV virus scanning on Gov.UK PaaS

# Clam AV virus scanning on Gov.UK PaaS

We use Clam AV to scan files as they are uploaded by users. This is implemented by creating a PaaS app that employs a ClamAV Docker image [built by the Home Office](https://github.com/cabinetoffice/docker-clamav). The image is hosted on [quay.io](quay.io/ukhomeofficedigital/clamav).

## Deployment

The PaaS app is a private app that will not be visible on the internet. To create the app:

```
cf create-app CLAMAV-PRIVATE-APP --app-type docker
```

A manifest-docker-clamav.yml file is created pointing to the Docker image with an apps.internal domain name for the private app.

```
---
applications:
  - name: my-docker-clamav
    memory: 1G
    disk_quota: 5G
    docker:
      image: quay.io/ukhomeofficedigital/clamav:latest
    routes:
    - route: CLAMAV-PRIVATE-APP.apps.internal
```

The AV app can then be deployed:

```
cf push CLAMAV-PRIVATE-APP -f manifest-docker-clamav.yml --strategy rolling
```

## Public app

So that the public app can communicate with the private AV app, an environmental variable needs to be set in the public apps manifest file that points to the private app:

```
---
applications:
  - name: my-public-app
    memory: 256M
    buildpacks:
    - python_buildpack
    env:
      AV_API: http://CLAMAV-PRIVATE-APP.apps.internal:8080
    ...
```

## App routing

In order to access the app, a [private route needs to be created](https://docs.cloud.service.gov.uk/deploying_apps.html#deploying-private-apps):

```
cf add-network-policy my-public-app my-docker-clamav --protocol tcp --port 8080
cf add-network-policy my-public-app my-docker-clamav --protocol tcp --port 3310
```

If you are routing from one workspace to another, use the -s flag:

```
cf add-network-policy my-public-app my-docker-clamav -s TARGET-WORKSPACE --protocol tcp --port 8080
cf add-network-policy my-public-app my-docker-clamav -s TARGET-WORKSPACE --protocol tcp --port 3310
```

## Scanning files

A form validator can be created to scan files (Python):
```
def fileVirusScan(form, field):
    if current_app.config['AV_API'] is None:
        return
    if (field.name not in request.files or request.files[field.name].filename == ''):
        return

    from pyclamd import ClamdNetworkSocket

    uploaded = request.files[field.name]
    uploaded.stream.seek(0)

    url = current_app.config['AV_API']
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    if url.index(':'):
        url = url[: url.index(':')]

    cd = ClamdNetworkSocket(host=url, port=3310, timeout=None)
    if not cd.ping():
        print('Unable to communicate with virus scanner', flush=True)
        return

    results = cd.scan_stream(uploaded.stream.read())
    if results is None:
        uploaded.stream.seek(0)
        return
    else:
        res_type, res_msg = results['stream']
        if res_type == 'FOUND':
            raise ValidationError('Virus found: %s' % res_msg)
        else:
            print('Error scanning uploaded file', flush=True)
```

## Testing

A sample file containing a test virus can be downloaded from [eicar.org](https://www.eicar.org/download-anti-malware-testfile/)
