#!/usr/bin/python3
"""
Fabric script to deploy .tgz archive to web servers
"""
from fabric.api import put, run, env
from os.path import exists

# Update with actual server IPs
env.hosts = ['54.162.233.113', '52.3.253.180']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploys an archive to web servers."""
    if not exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False

    try:
        file_name = archive_path.split("/")[-1]
        without_ext = file_name.split(".")[0]
        target_path = f"/data/web_static/releases/{without_ext}/"

        # Upload the archive
        put_result = put(archive_path, "/tmp/")
        if put_result.failed:
            print("Failed to upload file")
            return False

        # Commands to unpack and setup the deployment
        commands = [
            f"mkdir -p {target_path}",
            f"tar -xzf /tmp/{file_name} -C {target_path}",
            f"rm /tmp/{file_name}",
            f"mv {target_path}web_static/* {target_path}",
            f"rm -rf {target_path}web_static",
            "rm -rf /data/web_static/current",
            f"ln -s {target_path} /data/web_static/current"
        ]

        for cmd in commands:
            result = run(cmd)
            if result.failed:
                print(f"Command failed: {cmd}")
                return False

        print("Deployment successful")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
