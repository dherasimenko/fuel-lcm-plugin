#########################################################################
## FMSM - Fuel Master Service Monitoring - tracking manifests changes  ##
## re-run manifests execution via fuel task run                        ##
#########################################################################
import os
import checksum
import gitmgm
from gitmgm import GitMgm
import lcmconf
from lcmconf import LcmConf
import fuelclient
from fuelclient import client
from fuelclient.cli.actions.release import ReleaseAction
from fuelclient.objects.environment import Environment
from fuelclient.objects.node import Node
from fuelclient.objects.node import NodeCollection

# parameters from config file and web interface (future change to yaml)
remote = LcmConf().cfgread("GIT", "remote")
#local = LcmConf().cfgread("GIT", "local")
local = "/etc/puppet/" + client.APIClient.get_request("/version")['openstack_version'] + "/modules/osnailyfacter/modular/light-lcm"
native = "/etc/puppet/" + client.APIClient.get_request("/version")['openstack_version']
cluster_id = 1

class params:
	dir = native
	filepattern = "*tasks.yaml"
	tasks = [ "rsync_core_puppet" ]
	node = []

def git_fetch_manifests():
	if GitMgm().gitsync(remote,local) == True:
		if GitMgm().gitdiff(local) == True:
			ReleaseAction().sync_deployment_tasks(params)
			return 1
		else:
			return 0

def cluster_node_list():
	### get list on nodes assigned to cluster
	nodes = client.APIClient.get_request("/nodes?cluster_id=" + str(cluster_id))
	### make list of nodes which is online and provisioned
	for n in nodes:
		if n['online'] != False:
			if n['status'] == "ready" or n['status'] == "error" or n['status'] == "provisioned":
				params.node.append(n['id'])
				print params.node

def task_execute():
	if params.node != []:
		node_collection = NodeCollection.init_with_ids(params.node)
		Environment(cluster_id).execute_tasks(node_collection, params.tasks)
checksum.task_checksum(native,"generate")
if git_fetch_manifests() == 1:
	cluster_node_list()
	task_execute()
	checksum.task_checksum(native,"compare")

