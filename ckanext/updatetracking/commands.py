import sys
import os
import ckanapi
import ConfigParser
import time
from ckan.lib.cli import CkanCommand


class Update(CkanCommand):

    ''' Updates a resource with a daily tracking report
        Usage:
          update 
            - Updates the resource with the new tracking report
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        self._load_config()
	PATH = os.path.dirname(os.path.abspath(__file__))

	config = ConfigParser.RawConfigParser()
	config.read(PATH + '/updateconfig.cfg')
	FILENAME = config.get('DATASET','filename')
	DATASET = config.get('DATASET','dataset')
	SITE = config.get('CKAN','site')
	API = config.get('CKAN','api')
	
	try:
	    ckan = ckanapi.RemoteCKAN(SITE, apikey=API)
	except:
	    print("Ckan instance could not be initialized")
	    sys.exit()
	try:
	    dataset = ckan.action.package_show(id=DATASET)
	except:
	    print("Dataset: " + DATASET + " could not be found")
	    sys.exit()
	#try:
	#    file = open(FILENAME,'rb')
	#except:
	#    print("File was not found")
	    
	
	#Call the ckan tracking command
	os.system("cd /usr/lib/ckan/default/src/ckan && /usr/lib/ckan/default/bin/python /usr/lib/ckan/default/bin/paster tracking export " + FILENAME + " --config=/etc/ckan/default/production.ini")
	
	try:
	    file = open(FILENAME,'rb')
	except:
	    print("File was not generated")
	    sys.exit()
	for i in dataset["resources"]:
	    url = i["url"]
	    ckan.action.resource_update(id=i["id"],package_id=i["package_id"],url=i["url"],upload=file,name=file.name,format=i["format"])
	    #Trigger the datapusher hook the dirty way
	    ckan.action.resource_update(id=i["id"],package_id=i["package_id"],name=file.name,format=i["format"],url=i["url"]+"&")
	    ckan.action.resource_update(id=i["id"],package_id=i["package_id"],name=file.name,format=i["format"],url=url)
	
	sys.exit()
