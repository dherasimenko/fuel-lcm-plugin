Light Life Cycle Management Plugin
============

Compatible versions:
- Mirantis Fuel 7.0 and above

Abilities: 
- Fetch fuel tasks from git
- Check for difference and re-run tasks if it got a changes
- 

How to Build and Install:
- git clone git@github.com:openstack/fuel-plugin-light-lcm.git
- fpb --build ./fuel-plugin-nfs
- fuel plugins --install fuel-plugin-light-lcm-1.0-1.0.0-1.noarch.rpm

Requirements:
- GitPython
- HieraPy
- paramiko
- fuelclient
