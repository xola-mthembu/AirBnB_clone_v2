#!/usr/bin/python3
"""
Fabric script to clean up old archives.
"""
from fabric.api import local, run, env

# Define the environment
env.hosts = ['54.162.233.113', '52.3.253.180']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    :param number: Number of archives, including the most recent, to keep.
    """
    number = int(number) + 1
    # Formulate commands for local and remote cleanup
    local_cmd = ("ls -1t versions/web_static_*.tgz | "
                 "tail -n +{} | xargs rm -f".format(number))
    remote_cmd = ("ls -1t /data/web_static/releases/web_static_* | "
                  "tail -n +{} | xargs rm -rf".format(number))

    # Cleaning local archives
    local(local_cmd)

    # Cleaning remote archives
    run(remote_cmd)

# Example usage:
# fab -f 100-clean_web_static.py do_clean:number=2
