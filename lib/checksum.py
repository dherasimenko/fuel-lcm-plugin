import yaml
import os
import hashlib
import json
import lcmconf

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def task_checksum(mode):
	tasks_yaml = []
	for root, dirs, files in os.walk("./temp"):
	    for file in files:
	        if file.endswith("tasks.yaml"):
		     tasks_yaml.append(os.path.join(root, file))

	for task_yaml in tasks_yaml:
		with open(task_yaml, "rb") as f:
			for task in yaml.load(f.read()):
				if task['type'] == 'puppet':
					multi_file_hash = ''
					for f in  os.listdir(os.path.dirname(task['parameters']['puppet_manifest'])):
						if os.path.isfile(os.path.dirname(task['parameters']['puppet_manifest']) + "/" +f):
							single_file_hash = md5(os.path.dirname(task['parameters']['puppet_manifest']) + "/" +f)
							multi_file_hash = multi_file_hash + single_file_hash 
# future move data to database instead of config.ini
#					print json.dumps({'name' : task['id'], 'check_sum' : hashlib.md5(multi_file_hash).hexdigest() })
					if mode == "generate":
						lcmconf.LcmConf().cfgwrite("TASK_HASH",task['id'], hashlib.md5(multi_file_hash).hexdigest())
					elif mode == "compare":
						if lcmconf.LcmConf().cfgread("TASK_HASH",task['id']) != hashlib.md5(multi_file_hash).hexdigest():
							print "re-run puppet manifest " + task['id']
