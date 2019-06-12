## Currently Reading https://www.packtpub.com/web-development/flask-building-python-web-services

1. `firstapp` is a standard hello world
   1. Is spun up on a debain google cloud platform virtual image
   2. Runs a webserver using apache2 and uses flask to serve up the app
   3. A script for the python app named hello.py and a script for the virtual private server settings
named vps.py (which contains the debian and python package manager commands and config files to 
generate with notes)
2. `headlines` parses RSS feeds for dynamic routing
   1. A dictionary of feed urls trigger by URL path
   2. Four feeds are in the list BigML, Google ML news feeds, Top Reddit ML feeds, and MIT ML feeds
   3. each URL is `exampleDomain.com/bigml`, `exampleDomain.com/googl`, `exampleDomain.com/redit`, `exampleDomain.com/mit`

![flask_book.png](https://github.com/kayfay/flask-web-services/raw/master/flask_book.png)
