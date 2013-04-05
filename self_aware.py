#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013 David Grier

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys
import time
import pyrax
import pyxs

'''
This script is intended to run on boot and decide if this is first boot after a build action or a simple reboot

requires credentials file to contain:
[rackspace_cloud]
username = <CloudUserName>
api_key = <KEY>
'''

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

#Get my server id for use with the API from xenstore
myclient = pyxs.Client(xen_bus_path="/proc/xen/xenbus")

instance_uuid = myclient.read('name')
instance_uuid = "-".join(instance_uuid.split('-')[-5:])

#decide if I am online yet 
'''
Pseudocode
while not-successful in os.system("ping someip -c 4")
 time.sleep(1)
may be easier to place this in init scripts after network or depends on network
'''
print cs.servers.get(instance_uuid).status
#Am I a Build or Rebuild?
if ("BUILD" or "REBUILD") in cs.servers.get(instance_uuid).status:
  #wait until I have an active status
  while not "ACTIVE" in cs.servers.get(server.id).status:
    time.sleep(1)
  print "getting proper resolv.conf and putting it in place"
  #code to move or get files to put in place here
else:
  print "Looks like a normal reboot"
  sys.exit(0) 
	


