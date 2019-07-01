# Here we're using google-cloud-sdk, so install the sdk
# Create instance with gcloud instance create, enable with http
# ssh into gcloud via sdk and run the script or lines needed
# 	in this instance we can use to start and ssh into it
#  gcloud compute instances start instance-1 --zone=us-central1-a
#  gcloud compute ssh instance-1 --zone=us-central1-a

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# assuming <git-url> is git_repo_url to git repo for web_service.py app
web_service=web_service.py
git_repo=https://github.com/kayfay/flask-web-services.git
git_repo_url=flask-web-services

# configure vm as a webserver and for flask
# pip, apache webserver, apache web server gateway interface 
# git, flask, feedparser for rss
sudo apt-get update
sudo apt-get install python-pip apache libapache2-mod-wsgi git

# configure to process RSS feeds
pip install --user flask feedparser

# Setting webserver URL to /var/www
cd /var/www
sudo chown -R $USER /var/www

# Is the VPS fresh to download the repository or are we updating the dir
# in this case repo exists so no need to clone a repo when can pull
# git clone https://github.com/kayfay/flask-web-services.git
git pull
cd /var/www/flask-web-services/$web_service

# write out web_service.wsgi for webserver gateway interface
cat <<EOF > web_service.wsgi
import sys
sys.path.insert(0, "/var/www/flask-web-services/web_service")
from web_service import app as application
EOF

# write out apache config file to .wsgi
cd /etc/apache2/sites-available
sudo chown -R $USER /etc/apache2

# as a note, WSGIDaemonProcess may need as basis of requirements to 
# permissions of user or path require or not require additional flags
# e.g., WSGIDDaemonProcess web_service python-path=directory:directory and user=username
cat <<EOF > web_service.conf
<VirtualHost *>
        ServerName example.com

        WSGIScriptAlias / /var/www/flask-web-services/web_service/web_service.wsgi
        WSGIDaemonProcess web_service 
	<Directory /var/www/flask-web-services/web_service>
                WSGIProcessGroup web_service
                WSGIApplicationGroup %{GLOBAL}
                        Order deny,allow
                        Allow from all
        </Directory>
</VirtualHost>
EOF

# configure apache to serve flask as default index
sudo a2dissiet 000-default.conf
sudo a2ensite web_service.conf
sudo systemctl reload apache2 # manager varies by system

# monitor for error messages
sudo tail -f /var/log/apache2/error.log
