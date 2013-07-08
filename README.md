catmailer
=========

Sign up for cats in your inbox

## Installation
* Download the source, set up a virtualenv, and "workon" it.
* Run pip install -r requirements.always
* Install postfix/sendmail and MySQL
* Create a database for catmailer
* Open a python REPL and do
```
from catmailer import db
db.create_all()
```
* Copy local.py.default to local.py and fill in the appropriate hosts and passwords
