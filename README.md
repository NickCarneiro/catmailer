catmailer
=========
Enter your email and get cats in your inbox daily.

## Live Demo
http://cats.trillworks.com

## Installation
* Install dependencies: postfix, mysql, python-dev
* Download the source, set up a virtualenv, and "workon" it.
* Run pip install -r requirements.always
* Create a database for catmailer
* Open a python REPL and do

        from catmailer import db
        db.create_all()

* Copy local.py.default to local.py and fill in the appropriate hosts and passwords
* Configure your webserver to run catmailer.py
* Set up a cronjob to run send_cats.py

## Background
I wanted to learn Flask, so I built this. It's more interesting than a to-do app.

## Apache config

        <VirtualHost *:80>
        ServerName cats.trillworks.com
        WSGIDaemonProcess catmailer python-path=/path/to/catmailer:/home/you/.virtualenvs/catmailer/lib/python2.7/site-packages user=www-data group=www-data threads=5
        WSGIScriptAlias / /path/to/catmailer/catmailer.wsgi
        <Directory /path/to/catmailer>
                WSGIProcessGroup catmailer
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
            </Directory>
        </VirtualHost>
