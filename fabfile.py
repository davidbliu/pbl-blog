from fabric.api import *
from fabric_ec2 import EC2TagManager
import re
import yaml
import os

data = yaml.load(open('config.yaml', 'r'))

amazon_key = data['amazon_key']
amazon_secret = data['amazon_secret'] 
amazon_regions = data['amazon_regions']
keypair_location = data['keypair_path']

remote_vm_name = data['remote_vm_name']
ht_app_name = data['ht_app_name']

remote_public_dns = data['remote_public_dns']
remote_ht_app_volume = data['remote_ht_app_volume']
local_ht_app_volume = data['local_ht_app_volume']

def ec2_instances():
	tags = EC2TagManager(amazon_key, amazon_secret, regions= amazon_regions, common_tags={'Name': remote_vm_name})
	return tags.get_instances()
	

#
# setup which hosts to install on
#
def ht():
	hosts = ec2_instances()
	env.hosts = hosts
	env.user = 'ubuntu'
	env.container_name = ht_app_name
	env.key_filename = [keypair_location]
	print 'these are your hosts '+str(len(hosts))
	
@parallel
def backup_wp():
	print("Executing on %(host)s as %(user)s" % env)
	sudo('docker run --rm -v /usr/local/bin:/target jpetazzo/nsenter')
	pid = sudo('sudo docker inspect --format {{.State.Pid}} '+ env.container_name)
	with shell_env(PID=pid, FOO='david'):
		print 'backing up mysql database into app directory...'
		sudo("echo $PID")
		sudo('nsenter --target $PID --mount --uts --ipc --net --pid mysqldump wordpress > '+remote_ht_app_volume+'/dumpfile')
	print 'shipping app volume to local workstation...'
	local_ship_string = 'sudo scp -i '+keypair_location+' -r '+remote_public_dns+':'+remote_ht_app_volume+' '+local_ht_app_volume
	os.system(local_ship_string)
	print 'your wordpress has been backed up!'

@parallel
def restore_wp():
	print 'not implemented yet!'
	

#
# restores backed up wp locally on this machine
#
def local_restore_wp():
	