#!/usr/bin/env bash
# Sets up my web servers for the deployment of web_static
sudo apt-get -y update
sudo apt-get -y install nginx

mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | tee /data/web_static/releases/test/index.html > /dev/null

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu: /data/

nginx_config="/etc/nginx/sites-available/default"
if [ -e "$nginx_config" ]; then
    sudo sed -i '/server_name _;/a \\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }\n' "$nginx_config"
fi

service nginx restart
