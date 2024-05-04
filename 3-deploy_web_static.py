#!/usr/bin/python3
"""
Fabric script to handle both packing and deployment of web_static content
"""
from fabric.api import local, put, run, env
from datetime import datetime
import os

# Define the environment
env.hosts = ['54.162.233.113', '52.3.253.180']
env.user = 'ubuntu'
env.password = os.getenv('SSH_PASSWORD')


def do_pack():
    """
    Packs web_static files into a .tgz archive.
    :return: The archive path if successful, None otherwise.
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        print(f"An error occurred while packing: {e}")
        return None


def do_deploy(archive_path):
    """
    Deploys the archive to web servers.
    :param archive_path: The path to the .tgz file to be deployed
    :return: True if all operations are successful, False otherwise
    """
    if not os.path.isfile(archive_path):
        print(f"Archive not found: {archive_path}")
        return False

    try:
        file_name = archive_path.split("/")[-1]
        without_ext = file_name.split(".")[0]
        target_path = f"/data/web_static/releases/{without_ext}/"

        put_result = put(archive_path, "/tmp/")
        if put_result.failed:
            print("Failed to upload file")
            return False

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
            if run(cmd).failed:
                print(f"Command failed: {cmd}")
                return False

        print("Deployment successful")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False


def deploy():
    """
    Full deployment routine: pack and then deploy.
    """
    archive_path = do_pack()
    if archive_path is None:
        print("Failed to pack web_static")
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    # Start the full deployment process
    deploy()
