#
# What do these scripts do?
# copies files to and from remote amazon server
# run docker container on this host with the correct volume mounts (assume fresh)
# run docker container on t his host with correct volume mounts (assuming started elsewhere)
#

import yaml
import os

data = yaml.load(open('config.yaml', 'r'))

amazon_host = data['amazon_host']
local_mysql_volume = data['local_mysql_volume']
local_app_volume = data['local_app_volume']
remote_mysql_volume = data['remote_mysql_volume']
remote_app_volume = data['remote_app_volume']

#
# copies volumes from ec2 machine onto this host
#
def copy_mounts_here():

