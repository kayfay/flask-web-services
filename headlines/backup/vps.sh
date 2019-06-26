# Using google-cloud-sdk
# Install sdk
# Create instance with gcloud instance create; enable with http
# ssh into gcloud via sdk

# configure vm as a webserver and for flask
sudo apt-get update
sudo apt-get install python-pip
pip install --user flask
sudo apt-get install apache
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install git
# configure to process RSS feeds
pip install --user feedparser

# assuming <git-url> is gitrepourl to git repo for headlines.py app
gitrepourl='flask-web-services'
cd /var/www
sudo chown -R $USER /var/www
# the repository
# git clone https://github.com/kayfay/flask-web-services.git
# in this case repo exists so no need to clone a repo when can pull
git pull
cd /var/www/$gitrepourl/templates

# write out headlines.wsgi for webserver gateway interface
cat <<EOF > headlines.wsgi
import sys
sys.path.insert(0, "/var/www/flask-web-services/templates")
from headlines import app as application
EOF

# write out apache config file to .wsgi
cd /etc/apache2/sites-available
sudo chown -R $USER /etc/apache2
# as a note, WSGIDaemonProcess may need as basis of requirements to 
# permissions of user or path require or not require additional flags
# e.g., python-path=directory:directory and user=username
cat <<EOF > headlines.conf
<VirtualHost *>
        ServerName example.com

        WSGIScriptAlias / /var/www/flask-web-services/headlines/headlines.wsgi
        WSGIDaemonProcess headlines 
	<Directory /var/www/flask-web-services/headlines>
                WSGIProcessGroup headlines
                WSGIApplicationGroup %{GLOBAL}
                        Order deny,allow
                        Allow from all
        </Directory>
</VirtualHost>
EOF

# configure apache to serve flask as default index
sudo a2dissiet 000-default.conf
sudo a2ensite headlines.conf
sudo systemctl reload apache2 # manager varies by system

# monitor for error messages
sudo tail -f /var/log/apache2/error.log
