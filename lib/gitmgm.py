import git
import os
import shutil
import lcmconf

class GitMgm:
	def gitsync(self,remote_git, local_dir):
		if os.path.isdir(local_dir + "/.git"):
			git.cmd.Git(local_dir).pull("origin","master")
		else:
			if os.path.isdir(local_dir):
		    		shutil.rmtree(local_dir)
			os.mkdir(local_dir)
			repo = git.Repo.init(local_dir)
			origin = repo.create_remote('origin',remote_git)
			origin.fetch()
			origin.pull(origin.refs[0].remote_head)
			commit = git.Repo(local_dir).head.commit
			lcmconf.LcmConf().cfgwrite("GIT","commit", commit)
		return True

	def gitdiff(self,local_dir):
		repo = git.Repo(local_dir)
		latest_commit = repo.head.commit
		if str(latest_commit) != str(lcmconf.LcmConf().cfgread("GIT", "commit")):
			previews_commit = repo.commit("HEAD~1")
			lcmconf.LcmConf().cfgwrite("GIT","commit", git.Repo(local_dir).head.commit)
			return True
		else:
			return False


