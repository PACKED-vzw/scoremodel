The Scoremodel is a Python (Flask) application with MariaDB (MySQL) as back-end and Gunicorn as the WSGI HTTP Server.

## Requirements
* Python >= 3.4
* Flask
* Flask-SQLAlchemy
* Flask-Babel
* Flask-Login
* Flask-WTF
* bcrypt
* Markdown
* Flask-Markdown
* Gunicorn
* mysql-connector
* Flask-Testing

You can install all the dependencies (apart from Python itself) by executing `pip3 install -r requirements.txt` inside your virtual environment (see below).

## Installation
Download the latest version from [GitHub](https://github.com/PACKED-vzw/scoremodel) and unpack inside a directory on your hard drive (e.g. `/var/www/www.scoremodel.dev/scoremodel`).

For security reasons, it is best you create a user specific for the Scoremodel application (e.g. `scoremodel`). This user must own the directory you installed the application in.

### Virtual environment
Change to your application directory (`/var/www/www.scoremodel.dev/scoremodel`) and create a virtual environment.

```
cd /var/www/www.scoremodel.dev/scoremodel
virtualenv venv
. venv/bin/activate
```

Install your dependencies by executing `pip3 install -r requirements.txt`.

## Configuration
Copy `example_config.py` to `config.py` and update the following settings:

### Database
The application will create the required tables automatically, but you must create a database and a user beforehand.

* `DB_HOST`: your MySQL/MariaDB host.
* `DB_NAME`: name of the scoremodel database. This database must exist before you install the application.
* `DB_USER`: name of an (existing) user that can access the scoremodel database and can create tables.
* `DB_PASS`: password of the database user.

If your database server requires SSL for connections, you must also set `use_ssl` to `True` and update:

* `SSL_CA`: location of the CA file (in PEM format).
* `SSL_CERT`: location of the CERT file (in PEM format).
* `SSL_KEY`: location of the KEY file (in PEM format).

### Cross-Site-Request-Forgery protection
The scoremodel comes with CSRF-protection enabled by default, but it requires some setting up.

* `SECRET_KEY`: set this to a sufficiently long random string (e.g. from [https://www.grc.com/passwords.htm](https://www.grc.com/passwords.htm)).

### Multilingual
The application supports multiple languages. By default, all localisation is in English (_en_), but Dutch (_nl_) is also supported.

### Uploads

## Web server