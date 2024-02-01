#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the contents of the...
# web_static folder of your AirBnB Clone repo, using the function do_pack.

from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    # Create the folder versions if it doesn't exist
    local("mkdir -p versions")
    # Get the current datetime
    now = datetime.now()
    # Format the archive name with the datetime
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(now.year, now.month,
                                                        now.day, now.hour,
                                                        now.minute, now.second)
    # Compress the web_static folder to the archive name
    result = local("tar -cvzf versions/{} web_static".format(archive_name))
    # Return the archive path if successful, otherwise None
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
