import ConfigParser

class lcmconf:
	config_file = "./config.ini"
	conf = ConfigParser.ConfigParser()
	conf.read(config_file)

	def cfgread(self,section,option):
		return self.conf.get(section, option)

	def cfgwrite(self,section,option,value):
		self.conf.set(section,option,value)
		with open(self.config_file, 'wb') as configfile:
		    self.conf.write(configfile)

#remote = lcmconf().cfgread("GIT", "remote")
#local = lcmconf().cfgread("GIT", "local")
#lcmconf().cfgwrite("GIT","commit", "test3")
