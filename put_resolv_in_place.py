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
import time
import pyrax

'''
This script is intended to test that placing resolv.conf after server is in Active state is consistantly successful
 and can easily be modified to be a very basic drop file in after build complete for various uses
========
This script will 
-create a server based on an image with the configurable value of imgname
-add a public key to the server given the configurable value of keyfile
-out puts the server information as well as the contents of the resolv.conf file and the last lines of nova-agent.log
'''

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
imgname = 'testresolv'
size = 512

myimage = [img for img in cs.images.list()
                if imgname in img.name][0]
myflavor = [flavor for flavor in cs.flavors.list()
                if flavor.ram == size][0]

keyfile = os.path.expanduser('~/pubkey')

keyfileobj = open(keyfile, 'r')

resolvfile = os.path.expanduser('~/somedir/resolv')
files = {'/root/.ssh/authorized_keys': keyfileobj}

server_name='test1'
server = cs.servers.create(server_name, myimage.id, myflavor.id, files=files)
print "Name:", server.name
print "ID:", server.id
print "Status:", server.status
print "Admin Password:", server.adminPass
print "Waiting for Network config.."

while not cs.servers.get(server.id).networks:
  time.sleep(1)

mypubipv4 = [ ip for ip in cs.servers.get(server).networks['public']
                if len( ip.split(".") ) == 4 ]
mypubipv4 = str(mypubipv4[0])
print "Networks:", mypubipv4


print "waiting for active status"
while not "ACTIVE" in cs.servers.get(server.id).status:
  time.sleep(1)

print "rsyncing file"
os.system("rsync -avrz -e 'ssh -o StrictHostKeyChecking=no' " + resolvfile + " root@" + mypubipv4 + ":/etc/resolv.conf")
print "checking file:"
os.system("ssh root@" + mypubipv4 + " 'cat /etc/resolv.conf && tail -10 /var/log/nova-agent.log'")
