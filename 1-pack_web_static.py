from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates.tgz archive from the contents of the 'web_static' folder."""
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(date_time)
    archive_path = "versions/{}".format(archive_name)

    try:
        local("mkdir -p versions")  # Ensure the versions directory exists
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print("An error occurred: {}".format(e))
        return None
