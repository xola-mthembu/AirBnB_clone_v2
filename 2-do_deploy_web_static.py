#!/usr/bin/python3
"""
Fabric script
"""
from fabric.api import env, put, run
import os

env.hosts = ['54.162.233.113', '52.3.253.180']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    The archive is uploaded to the /tmp/ directory on the web server.
    It is then extracted to the /data/web_static/releases/<archive filename
    without extension> directory.
    The symbolic link /data/web_static/current is updated to point to the new
    release directory.

    Args:
        archive_path (str): The path of the archive file to be deployed.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/{}/".format(no_ext)
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(path))
        return True
    except Exception:
        return False
