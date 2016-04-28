import gitmgm
import lcmconf
import os
import paramiko
import json
import fuelclient
from fuelclient import client
from fuelclient.cli.actions.release import ReleaseAction
from fuelclient.objects.environment import Environment
from fuelclient.objects.node import Node
from fuelclient.objects.node import NodeCollection

remote = lcmconf.lcmconf().cfgread("GIT", "remote")
local = lcmconf.lcmconf().cfgread("GIT", "local")
cluster_id = 1

class params:
	dir = local
	filepattern = "*tasks.yaml"
	tasks = [ "rsync_core_puppet" ]
	node = []

if gitmgm.GitMgm().gitsync(remote,local) == True:
	if gitmgm.GitMgm().gitdiff(local) == True:
		ReleaseAction().sync_deployment_tasks(params)
		print "manifest_sync executed"
	else:
		print "all set"

### get list on nodes assigned to cluster
nodes = client.APIClient.get_request("/nodes?cluster_id=" + str(cluster_id))
### make list of nodes which is online and provisioned
for n in nodes:
	if n['online'] != False:
		if n['status'] == "ready" or n['status'] == "error" or n['status'] == "provisioned":
			params.node.append(n['id'])


if params.node != []:
	node_collection = NodeCollection.init_with_ids(params.node)
	Environment(cluster_id).execute_tasks(node_collection, params.tasks)
