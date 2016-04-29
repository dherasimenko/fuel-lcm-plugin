import yaml
import os
import hashlib
from os.path import normpath, walk, isdir, isfile, dirname, basename, \
    exists as path_exists, join as path_join

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


tasks_yaml = []
for root, dirs, files in os.walk("./temp"):
    for file in files:
        if file.endswith("tasks.yaml"):
	     tasks_yaml.append(os.path.join(root, file))

for task_yaml in tasks_yaml:
	with open(task_yaml, "rb") as f:
		for task in yaml.load(f.read()):
			if task['type'] == 'puppet':
				if task['id'] == 'hiera':
					print task['parameters']['puppet_manifest']
					print md5(task['parameters']['puppet_manifest'])

