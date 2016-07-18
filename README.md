# ckanext-updatetracking
Uses the CKAN tracking export to CSV command and uploads it to a resource

Installing
NB! This module is developed on CKAN v2.5.2, compatibility with other version is not ensured

### Activate virtualenv
```
source /usr/lib/ckan/default/bin/activate
cd /usr/lib/ckan/default/src
git clone git@github.com:NicolaiMogensen/ckanext-updatetracking.git
cd ckanext-updatetracking
```

### Install Extension
```
python setup.py develop

```
### Enable plugin in configuration
```
 sudo nano /etc/ckan/default/production.ini
 ckan.plugins = datastore ... updatetracking
```
## Usage
Fill in the ``updateconfig.cfg`` with the appropriate values like so
```
[DATASET]
dataset= Your CKAN dataset ID (examples: tracking or site-usage)
filename=tracking.csv

[CKAN]
api= Your ckan API key, must be able to update the given resource
site= Your CKAN site (example: http://demo.ckan.org)

```
The extension creates a command for periodical update of the Datastore. To execute the command periodically, add following cron job:

### Cron job daily at 03:55
```
55 3 * * * cd /usr/lib/ckan/default/src/ckanext-updatetracking && /usr/lib/ckan/default/bin/python /usr/lib/ckan/default/bin/paster update --config=/etc/ckan/default/production.ini
```

