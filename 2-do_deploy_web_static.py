#!/usr/bin/python3
# Fabric script that distributes an archive to your web servers,
# using the function do_deploy

from fabric.api import env, put, run
from os.path import exists

# Define the hosts and the user
env.hosts = ['35.174.204.152', '100.26.133.61']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    # Check if the archive path exists
    if not exists(archive_path):
        return False
    # Get the archive filename without the extension
    archive_file = archive_path.split('/')[-1]
    archive_name = archive_file.split('.')[0]
    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, '/tmp/{}'.format(archive_file))
    # Uncompress the archive to the folder /data/web_static/releases/
    # <archive filename without extension> on the web server
    run('mkdir -p /data/web_static/releases/{}'.format(archive_name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'
        .format(archive_file, archive_name))
    # Delete the archive from the web server
    run('rm /tmp/{}'.format(archive_file))
    # Delete the symbolic link /data/web_static/current from the web server
    run('rm -rf /data/web_static/current')
    # Create a new the symbolic link /data/web_static/current on the web server
    # linked to the new version of your code
    run('ln -s /data/web_static/releases/{} /data/web_static/current'
        .format(archive_name))
    # Return True if all operations have been done correctly, otherwise False
    return True
