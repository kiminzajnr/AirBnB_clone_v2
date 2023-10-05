#!/usr/bin/env bash
# Sets up my web servers for the deployment of web_static
sudo apt-get -y update
sudo apt-get -y install nginx

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    <h1>Hello World!!!!!<h1>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu: /data/

print %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	server_name _;
	add_header X-Served-By $HOSTNAME;

	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html;
	}
}" > /etc/nginx/sites-enabled/default

sudo service nginx restart
