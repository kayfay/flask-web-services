# Using google-cloud-sdk
# Install sdk
# Create instance with gcloud instance create; enable with http
# ssh into gcloud via sdk

# configure vm
sudo apt-get update
sudo apt-get install python-pip
pip install --user flask
sudo apt-get install apache
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install git

# assuming <git-url> is gitrepourl to git repo for hello.py
gitrepourl='flask-web-services'
cd /var/www
# clone into vps or git pull
git clone https://github.com/kayfay/flask-web-services.git
sudo chown -R $USER /var/www
cd /var/www/$gitrepourl/firstapp

# write out hello.wsgi for webserver gateway interface
cat <<EOF > hello.wsgi
import sys
sys.path.insert(0, "/var/www/flask-web-services/firstapp")
from hello import app as application
EOF

# write out apache config file to .wsgi
cd /etc/apache2/sites-available
sudo chown -R $USER /etc/apache2
# as a note, WSGIDaemonProcess may need as basis of requirements to 
# permissions of user or path require or not require additional flags
# e.g., python-path=directory:directory and user=username
cat <<EOF > hello.conf
<VirtualHost *>
        ServerName example.com

        WSGIScriptAlias / /var/www/flask-web-services/firstapp/hello.wsgi
        WSGIDaemonProcess hello
	<Directory /var/www/flask-web-services/firstapp>
                WSGIProcessGroup hello
                WSGIApplicationGroup %{GLOBAL}
                        Order deny,allow
                        Allow from all
        </Directory>
</VirtualHost>
EOF

# configure apache to serve flask as default index
sudo a2dissiet 000-default.conf
sudo a2ensite hello.conf
sudo systemctl apache2 reload

# monitor for error messages
sudo tail -f /var/log/apache2/error.log
