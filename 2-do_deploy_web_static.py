#!/usr/bin/python3

"""
 Fabric script that generates a .tgz archive from the contents of the
 web_static folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import run, env, run, put, sudo, local
import os.path
from datetime import datetime
""" Importing the required modules"""


def do_pack():
    """ Function to help to generate the archive"""

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")

    local("mkdir -p versions")

    archive_name = f"versions/web_static_{year}{month}{day}{hour}\
{minute}{second}.tgz"
    # capture the result
    result = local(f"tar -czvf {archive_name} web_static", capture=True)

    if result.failed:
        return None
    else:
        return archive_name


"""
Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy:
"""

env.hosts = ['100.26.243.45', '54.236.24.205']


def do_deploy(archive_path):
    """ Distributes an archive to the web servers"""

    if os.path.isfile(archive_path) is False:
        return False
    try:
        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        archive_filename = archive_path.split("/")[-1]
        archive_name = archive_filename.split(".")[0]
        remove_folder = '/data/web_static/releases/{archive_name}/web_static/*'
        # check if the code is running locally or on remote hosts
        run_locally = os.getenv("run_locally", None)
        if run_locally is None:
            # local(f'rm -rf /data/web_static/releases/{archive_name}/')
            local(f'mkdir -p /data/web_static/releases/{archive_name}')
            local(f'tar -xzf {archive_path} -C\
 /data/web_static/releases/{archive_name}/')

            local(f'mv /data/web_static/releases/{archive_name}/web_static/* '
                  f'/data/web_static/releases/{archive_name}/')
            local(f'rm -rf {remove_folder}')
            local(f'rm -rf /data/web_static/current')
            local(f'rm -rfR /data/web_static/current')
            local(f'ln -s /data/web_static/releases/{archive_name}/\
 /data/web_static/current')
            os.environ['run_locally'] = "True"

        # Upload the archive to the /tmp/ directory of the web server

        put(archive_path, f'/tmp/{archive_filename}')
        run(f'rm -rf /data/web_static/releases/{archive_name}/')
        run(f'mkdir -p /data/web_static/releases/{archive_name}/')
        run(f'tar -xzf /tmp/{archive_filename} -C\
 /data/web_static/releases/{archive_name}/')
        # Delete the archive from the web server
        run(f'rm /tmp/{archive_filename}')

        run(f'mv /data/web_static/releases/{archive_name}/web_static/* '
            f'/data/web_static/releases/{archive_name}/')

        run(f'rm -rf /data/web_static/releases/{archive_name}/web_static/*')
        # Delete the symbolic link /data/web_static/current from the web server
        run(f'rm -rf /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current on the
        # web server linked to the new version of your code (/data/web_static/
        # releases/<archive filename without extension>)

        run(f'ln -s /data/web_static/releases/{archive_name}/\
 /data/web_static/current')

        # Returns True if all operations have been done correctly,
        # otherwise returns False
        return True
    except Exception:
        return False
