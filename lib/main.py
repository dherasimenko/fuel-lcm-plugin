import gitmgm
import lcmconf
import os
import paramiko
import json
import fuelclient
from fuelclient import client

remote = lcmconf.lcmconf().cfgread("GIT", "remote")
local = lcmconf.lcmconf().cfgread("GIT", "local")

if gitmgm.GitMgm().gitsync(remote,local) == True:
	if gitmgm.GitMgm().gitdiff(local) == True:
		print "manifest_sync executed"
	else:
		print "all set"

nodes = client.APIClient.get_request("/nodes?cluster_id=1")
for node in nodes:
	print node["ip"]
