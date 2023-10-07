#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy
"""
import time
import os
from fabric.api import *
from fabric.operations import run, put


env.hosts = ['100.26.243.45', '54.236.24.205']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/priv.key'


def do_pack():
    """generates a .tgz archive"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return "versions/web_static_{:s}.tgz".\
            format(time.strftime("%Y%m%d%H%M%S"))
    except BaseException:
        return None


# def do_deploy(archive_path):
#     """distributes an archive to my web servers"""
#     if not os.path.exists(archive_path):
#         return False
#     try:
#         # Upload archive
#         put(archive_path, '/tmp/')
#         archive_filename = archive_path.split('/')[-1]
#         archive_name_noext = archive_filename.split('.')[0]
#         release_path = f"/data/web_static/releases/{archive_name_noext}"
#         run(f"mkdir -p {release_path}")
#         run(f"tar -xzf /tmp/{archive_filename} -C {release_path}")

#         run(f"rm /tmp/{archive_filename}")

#         run("rm /data/web_static/current")

#         run(f"ln -s {release_path} /data/web_static/current")

#         return True
#     except Exception as e:
#         return False

def do_deploy(archive_path):
    """ Distributes an archive to the web servers"""

    if os.path.isfile(archive_path) is False:
        return False
    try:
        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        archive_filename = archive_path.split("/")[-1]
        archive_name = archive_filename.split(".")[0]
        remove_folder = f'/data/web_static/releases/\
            {archive_name}/web_static/*'
        # check if the code is running locally or on remote hosts
        run_locally = os.getenv("run_locally", None)
        if run_locally is None:
            # local(f'rm -rf /data/web_static/releases/{archive_name}/')
            local(f'mkdir -p /data/web_static/releases/{archive_name}')
            local(f'tar -xzf {archive_path} -C\
 /data/web_static/releases/{archive_name}/')

            local(f'mv /data/web_static/releases/\
{archive_name}/web_static/* '
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
