import docker
import os

docker_client = docker.Client(base_url='unix://var/run/docker.sock',
                  version='1.11',
                  timeout=10)

# APP_HOST_VOLUME_PATH = '/home/david/volumes/blog_app1'
# MYSQL_HOST_VOLUME_PATH = '/home/david/volumes/blog_mysql1'

# DATA_CONTAINER_NAME = 'blog_data_container'
# MAIN_CONTAINER_NAME = 'blog_container'

# MYSQL_TRANSFER_VOLUME = '/home/david/volumes/blog_mysql_transfer'

APP_HOST_VOLUME_PATH = '/home/david/volumes/ht_app/ht_app'
MYSQL_HOST_VOLUME_PATH = '/home/david/volumes/ht_mysql/ht_mysql'

DATA_CONTAINER_NAME = 'ht_data_container'
MAIN_CONTAINER_NAME = 'ht_container'

MYSQL_TRANSFER_VOLUME = '/home/david/volumes/ht_mysql/ht_mysql'
#
# create data volume container if not exists
#
# 
def initialize_data_container():
	docker_client.remove_container('blog_data_container')
	data_container = docker_client.create_container(image='ubuntu', command='printenv', hostname=None, user=None,
	                   detach=False, stdin_open=False, tty=False,volumes=['/var/lib/mysql', '/app'],
	                   ports=None, environment=None, dns=None,
	                   volumes_from=None, network_disabled=False, name='blog_data_container',
	                   entrypoint=None, cpu_shares=None, working_dir=None)
	docker_client.start(data_container, binds = {MYSQL_HOST_VOLUME_PATH:'/var/lib/mysql', APP_HOST_VOLUME_PATH:'/app'})
	print data_container

def initialize_app_data():
	initialize_string = 'sudo docker run -v '+APP_HOST_VOLUME_PATH+':/backup/app tutum/wordpress cp -a /app /backup'
	os.system(initialize_string)
#
# create actual container
#
def initialize_blog_container():
	try:
		docker_client.stop(MAIN_CONTAINER_NAME, timeout = 50000)
		docker_client.remove_container(MAIN_CONTAINER_NAME)
	except Exception as failure:
		print failure
	run_string = 'sudo docker run -d -p 5130:80 --name blog_container --volumes-from blog_data_container tutum/wordpress'
	os.system(run_string) 


def start_fresh_wordpress():
	initialize_app_data()
	initialize_data_container()
	initialize_blog_container()

# dont create new volume stuff
def reconnect_wordpress():
	initialize_blog_container()

'''
procedure:
	have app folder and old db volume 
	change over
'''
def prepare_newserver():
	print 'preparing files for server location change...'
	#
	# make new db volume
	#
	print '\n\n'
	# run_string = 'sudo docker run  -i -t -v '+MYSQL_TRANSFER_VOLUME+':/var/lib/mysql -v '+APP_HOST_VOLUME_PATH+':/app tutum/wordpress bash'
	run_string = 'sudo docker run  -i -t -v '+MYSQL_TRANSFER_VOLUME+':/var/lib/mysql tutum/wordpress bash'

	# app volume can remain the same
	print run_string
	print '\n\n'
	print 'mysql wordpress < /app/backup'
	print '\n\n'
	# push new volumes to s3


def nsenter():
	os.system('sudo docker run --rm -v /usr/local/bin:/target jpetazzo/nsenter')
	pid_find_string = 'sudo PID=$(sudo docker inspect --format {{.State.Pid}} '+MAIN_CONTAINER_NAME+')'
	print 'now enter this command'
	print 'wait for it'
	print ''
	print pid_find_string+';sudo nsenter --target $PID --mount --uts --ipc --net --pid'
	print ''
	print 'mysqldump wordpress > /app/backup'
	print ''

nsenter()
# prepare_newserver()