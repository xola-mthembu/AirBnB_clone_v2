#!/usr/bin/python3
"""
Fabric script to generate .tgz archive from the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generate .tgz archive from the web_static folder."""
    try:
        local("mkdir -p versions")  # Ensure the target directory exists
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
