# Installation instructions

This document provides instructions for the installation of the Scoremodel on a Ubuntu-based Linux system. It should work on most other Linux systems without modifications.

The Scoremodel is a Python (Flask) application usually served via Gunicorn with MySQL or MariaDB as a back-end. It will only work with Python 3.4+.

## Requirements
* Python >= 3.4

All other requirements can be installed by executing `pip3 install -r requirements.txt` inside your virtual environment (see below). Note that `mysql-connector` requires some header files that aren't always available. Should you run in to issues, it is best to install it globally via your distribution package manager (e.g. `apt-get install python3-mysql.connector`).

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

### Installing `mysql-connector`

Since version 2.2.3, installing `mysql-connector` requires some extra steps (instructions for Ubuntu).

1. Install required OS packages:

```
apt-get install libprotobuf-dev libprotobuf9v5 protobuf-compiler
```

2. Set environment variables _in the shell you will be using to install your requirements_:

```
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=/usr/include/google/protobuf && export MYSQLXPB_PROTOBUF_LIB_DIR=/usr/lib/x86_64-linux-gnu && export export MYSQLXPB_PROTOC=/usr/bin/protoc

```

## Installation
The Scoremodel will create its own database, so the only installation step you have to perform is to download the latest version from [GitHub](https://github.com/PACKED-vzw/scoremodel) and unpack it inside a directory on your hard drive (e.g. `/var/www/www.scoremodel.dev/scoremodel`).

For security reasons, it is best you create a user specific for the Scoremodel application (e.g. `scoremodel`). This user must own the directory you installed the application in.

### Virtual environment
While the app will work if you install its dependencies globally, for security reasons you are advised to use a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Change to your application directory (`/var/www/www.scoremodel.dev/scoremodel`) and create a virtual environment.

```
cd /var/www/www.scoremodel.dev/scoremodel
virtualenv venv
. venv/bin/activate
```

Go back to the previous directory with `cd ..` and install the dependencies by executing `pip3 install -r requirements.txt`.

## Configuration
Before the setup can be started, you must first configure the application in `config.py`.

Copy `example_config.py` to `config.py` and update the following settings:

### Database
The application will create the required tables automatically, but you must create a database and a database user beforehand.

After you have created them, set the following parameters in `config.py` to the correct value.

* `DB_HOST`: your MySQL/MariaDB host.
* `DB_NAME`: name of the scoremodel database. This database must exist before you install the application.
* `DB_USER`: name of a user that can access the scoremodel database and can create tables.
* `DB_PASS`: password of the database user.

If your database server requires SSL for connections, you must also set `use_ssl` to `True` and update:

* `SSL_CA`: location of the CA file (in PEM format).
* `SSL_CERT`: location of the CERT file (in PEM format).
* `SSL_KEY`: location of the KEY file (in PEM format).

### Cross-Site-Request-Forgery protection
The scoremodel comes with CSRF-protection enabled by default, but it requires a `SECRET_KEY` before it will work.

* `SECRET_KEY`: set this to a sufficiently long random string (e.g. from [https://www.grc.com/passwords.htm](https://www.grc.com/passwords.htm)).

## Other configuration settings
It is normally not necessary to change the other settings in the configuration file.

### Uploads
Uploads are supported, and stored in the `UPLOAD_FOLDER`. Sometimes it can be necessary to change the accepted file types. This can be done in `ALLOWED_EXTENSIONS`. If you want to raise (or lower) the maximum file size, set `MAX_CONTENT_LENGTH` (in bytes).

### Multilingualism
The application supports a multilingual interface. All languages in `LANGUAGES` are supported. If you want to change the default language, pick one of them and set `BABEL_DEFAULT_LOCALE` to it.

Note that the app will only show content that is available in the selected language. It will return a `404 Not Found` if you try to access content that doesn't exist in the selected language, even if it does in other languages.

## Web server
The app is designed to use the Gunicorn HTTP server, which you can reverse proxy behind an Apache HTTP web server.

### Gunicorn
#### Manual
Change to the directory that contains the Scoremodel (e.g. `/var/www/dev.scoremodel.org/scoremodel`) and start the Gunicorn server with 4 workers running on port 8081 and posting all output to `gunicorn_error.log`:

```
gunicorn -w 4 -b 127.0.0.1:8081 scoremodel:app --timeout 240 --graceful-timeout 240 --capture-output --error-logfile gunicorn_error.log
```

#### Supervisor (automatic)
While you can start it manually and leave it running in `screen`, this is rather error-prone. Better is to use a process manager like [supervisor](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps). The script `supervisor.sh` can be used as the command inside your supervisor configuration. It will start the Gunicorn server automatically.

Adapt this sample configuration (in `/etc/supervisor.d/`) to your needs:
```
[program:scoremodel]
directory   = /var/www/dev.scoremodel.org/scoremodel
command     = bash supervisor.sh
user        = scoremodel
autostart   = true
autorestart = true
```

To start the application, execute:

```
supervisorctl reread # Only after you changed the configuration file
supervisorctl start
```

### Apache
We use a Apache HTTP server as a reverse proxy, but you could use an alternative as well. You can even let Gunicorn run directly on port 80, but this isn't recommended.

The sample configuration file creates a [name-based Virtual Host](https://httpd.apache.org/docs/current/vhosts/examples.html) on _dev.scoremodel.org_ at port 80.
```
<VirtualHost *:80>
  ServerName dev.scoremodel.org

  ## Vhost docroot
  DocumentRoot "/var/www/dev.scoremodel.org/html"

  <Directory "/var/www/dev.scoremodel.org/html">
    AllowOverride All
    Require all denied
  </Directory>

  ## Logging
  ErrorLog "/var/log/apache2/dev.scoremodel.org_80_error.log"
  ServerSignature Off
  CustomLog "/var/log/apache2/dev.scoremodel.org_80_access.log" combined

  ## Reverse proxy
  ProxyPass / http://localhost:8081/
  ProxyPassReverse / http://localhost:8081/
  ProxyPreserveHost On

</VirtualHost>
```

The last three lines (starting with `Proxy`) configure the Apache reverse proxy that allows you to serve the app via the normal port 80, while internally running on port 8081.

Enable the website by executing:
```
a2ensite dev.scoremodel.org.conf # The name of the configuration file you configured the Virtual Host in
service apache2 reload
```

## Additional actions
Before running the setup, several steps must be taken to ensure a smooth experience.

* Either create the `logs` directory or update the location of the log file in the configuration settings.
* In `/scoremodel/static/lib`, execute `bower install` to install the Javascript dependencies (found in `bower.json`).

## Setup
After you have configured the database and web server, you can visit the application at the web address you specified (e.g. dev.scoremodel.org).

If the app detects that tables are missing, or there is no administrative user, it will automatically start the setup. All required tables and settings will automatically be created, as well as an administrative user. You will be provided with a username and an automatically generated password. It is recommended to change it, but it is never stored anywhere.

After the setup completes, the application is ready to use.
