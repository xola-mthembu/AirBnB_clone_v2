#!/usr/bin/python3
"""
Fabric script to generate a compressed .tgz archive from the web_static folder.
Script used for packaging web_static content for deployment or backup purposes.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz archive from the web_static folder.
    This function creates a timestamped archive of the web_static folder
    and returns the path to the created archive.
    """
    try:
        # Ensure the target directory exists
        local("mkdir -p versions")
        # Generate a timestamp in the format YYYYMMDDHHMMSS
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # Construct the archive path
        archive_path = f"versions/web_static_{timestamp}.tgz"
        # Create the archive by compressing the web_static folder
        local(f"tar -cvzf {archive_path} web_static")
        # Return the path to the created archive
        return archive_path
    except Exception as e:
        # Print an error message with the exception details
        print(f"An error occurred: {e}")
        # Return None to indicate an error occurred
        return None
