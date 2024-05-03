#!/usr/bin/env bash
# Configures web servers for the deployment of web_static.

# Check if Nginx is installed
if ! dpkg -l | grep -qw nginx; then
    echo "Nginx is not installed. Installing Nginx."
    # Update and install Nginx if it isn't installed
    if ! sudo apt-get update || ! sudo apt-get -y install nginx; then
        echo "Failed to install Nginx."
        exit 1
    fi
else
    echo "Nginx is already installed."
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file and check for success
if ! echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null; then
    echo "Failed to create index.html."
    exit 1
fi

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Check if the ubuntu user exists and change ownership accordingly
if id "ubuntu" &>/dev/null; then
    sudo chown -R ubuntu:ubuntu /data/
else
    echo "User 'ubuntu' does not exist. Using root instead."
    sudo chown -R root:root /data/
fi

# Clean any existing '/hbnb_static/' configuration before adding new configuration
if grep -q "location /hbnb_static/" /etc/nginx/sites-available/default; then
    sudo sed -i '/location \/hbnb_static/,/}/d' /etc/nginx/sites-available/default
fi

# Update the Nginx configuration to serve the content
sudo sed -i '/server_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Check Nginx configuration for syntax errors
if ! sudo nginx -t; then
    echo "Nginx configuration error."
    exit 1
fi

# Restart Nginx to reload the configuration
if ! sudo service nginx restart; then
    echo "Failed to restart Nginx."
    exit 1
fi

echo "Nginx configuration completed successfully."
