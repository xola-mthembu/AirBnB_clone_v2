#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/{}".format(no_ext)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(filename, path))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}/".format(path, path))
        run("rm -rf {}/web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        print('New version deployed!')
        return True
    except:
        return False
