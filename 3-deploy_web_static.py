#!/usr/bin/python3
# Fabric script that creates and distributes an archive to your web servers,
# using the function deploy
# Based on the file 2-do_deploy_web_static.py

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists

# Define the hosts and the user
env.hosts = ['35.174.204.152', '100.26.133.61']
env.user = 'ubuntu'

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    # Create the folder versions if it doesn't exist
    local("mkdir -p versions")
    # Get the current datetime
    now = datetime.now()
    # Format the archive file name with the datetime
    archive_file_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    # Compress the web_static folder to the archive file name
    result = local("tar -cvzf versions/{} web_static".format(
        archive_file_name))
    # Return the archive path if successful, otherwise None
    if result.succeeded:
        return "versions/{}".format(archive_file_name)
    else:
        return None

def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    # Check if the archive path exists
    if not exists(archive_path):
        return False
    # Get the archive file name without the extension
    archive_file_name = archive_path.split('/')[-1]
    archive_name = archive_file_name.split('.')[0]
    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, '/tmp/{}'.format(archive_file_name))
    # Uncompress the archive to the folder /data/web_static/releases/
    # <archive name> on the web server
    run('mkdir -p /data/web_static/releases/{}'.format(archive_name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
        archive_file_name, archive_name))
    # Delete the archive from the web server
    run('rm /tmp/{}'.format(archive_file_name))
    # Delete the symbolic link /data/web_static/current from the web server
    run('rm -rf /data/web_static/current')
    # linked to the new version of your code
    run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(
        archive_name))
    # Return True if all operations have been done correctly, otherwise False
    return True

def deploy():
    """Creates and distributes an archive to your web servers."""
    # Call the do_pack() function and store the path of the created archive
    archive_path = do_pack()
    # Return False if no archive has been created
    if archive_path is None:
        return False
    result = do_deploy(archive_path)
    # Return the return value of do_deploy
    return result
