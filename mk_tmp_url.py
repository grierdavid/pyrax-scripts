#!/usr/bin/env python

import os
import pyrax

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(cred_file)

cf = pyrax.cloudfiles

my_key = 'nv6ZSTBeNJtef85' 
secs = 24 * 60 * 60
my_container = 'container_name'
my_obj = 'object_name'

cf.set_temp_url_key(my_key)

url = cf.get_temp_url(my_container, my_file, seconds=secs, method="GET")

print url

