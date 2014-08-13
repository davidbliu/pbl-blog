PBL-Blog
========

Blog Plugin for core PBL Portal

# Backup Procedure

__on remote machine__
* `nsenter` running container
	* `sudo docker run --rm -v /usr/local/bin:/target jpetazzo/nsenter`
	* `PID=$(docker inspect --format {{.State.Pid}} <container_name_or_ID>)`
	* `nsenter --target $PID --mount --uts --ipc --net --pid`
* backup database to /app/backup_<uid>
	* `mysql wordpress < /app/backup`

__on work machine__
* transfer files to safe location (my machine for now)
	* `scp -r user@remote:src_directory dst_directory`
* find and replace IPs in `/app/backup`
* start container with clean mysql mount but old app mount, run with `bash` option
	* `docker run -i -t -v <app_mount_path>:/app tutum/wordpress bash`
	* ``./run.sh &`
	* restore mysql database from  `/app/backup`
	* `mysql wordpress < /app/backup`
* start `-d` real container with mounts to __app__ _and_ __mysql__
	* `docker run -d -p <port>:80 -v <mysql_mount>:/var/lib/mysql -v <app_mount_>:/app tutum/wordpress /run.sh`

# Interface

# Box Integration