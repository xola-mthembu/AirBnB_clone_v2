#!/usr/bin/python3
"""
Fabric script to deploy .tgz archive to web servers
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']  # replace with your actual IPs
env.user = 'ubuntu'  # adjust as per your server settings


def do_deploy(archive_path):
    """Deploys an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        without_ext = file_name.split(".")[0]
        target_path = f"/data/web_static/releases/{without_ext}/"

        # Upload the archive
        put(archive_path, "/tmp/")

        # Unpack the archive
        run(f"mkdir -p {target_path}")
        run(f"tar -xzf /tmp/{file_name} -C {target_path}")

        # Remove the archive from the server
        run(f"rm /tmp/{file_name}")

        # Move contents out of the web_static subfolder
        run(f"mv {target_path}web_static/* {target_path}")
        run(f"rm -rf {target_path}web_static")

        # Update the symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {target_path} /data/web_static/current")

        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
