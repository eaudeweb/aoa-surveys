AOA Surveys
===========

.. contents ::

Project Name
------------

Prerequisites - System packages
-------------------------------

These packages should be installed as superuser (root).

Debian based systems
~~~~~~~~~~~~~~~~~~~~
Install these before setting up an environment::

    apt-get install python-setuptools python-dev libmysqlclient-dev \
    python-virtualenv mysql-server git


RHEL based systems
~~~~~~~~~~~~~~~~~~
Install Python2.7 with PUIAS: https://gist.github.com/nico4/9616638

Run these commands::

    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7 -
    pip2.7 install virtualenv
    yum install mysql-server mysql git mysql-devel


Product directory
-----------------


Install dependencies
--------------------
We should use Virtualenv for isolated environments. The following commands will
be run as an unprivileged user in the product directory::

1. Clone the repository::

    git clone git@github.com:eaudeweb/aoa-surveys.git -o origin aoa-surveys 
    cd aoa-surveys

2.1. Create & activate a virtual environment::

    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

2.2 Make sure setuptools >= 0.8 is installed::

    pip install -U setuptools

2.3 Create an instance folder for file uploads::

    mkdir instance

3. Install dependencies::

    pip install -r requirements-dep.txt

4. Create a local configuration file::

    cd aoasurveys
    cp local_settings.py.example local_settings.py

    # Follow instructions in local_settings.py to adapt it to your needs.

6. Set up the MySQL database::

    # Replace [user] and [password] with your MySQL credentials and [db_name]
    # with the name of the database:

    mysql -u[user] -p[password] -e 'create database [db_name] CHARACTER SET utf8 COLLATE utf8_general_ci;'

   **The database charset MUST be utf8.**

7. Update local configuration file with database credentials and database name
   - ``default`` section in ``DATABASES`` dict.

8. Create initial database structure::

    ./manage.py syncdb

9. Load initial fixtures::

    ./manage.py loaddata aoasurveys/fixtures/forms.json

10. Collect static assets::

    ./manage.py collectstatic --noinput



Development hints
=================

Requirements
------------

Use ``requirements-dev.txt`` instead of ``requirements-dep.txt``::

    pip install -r requirements-dev.txt

Command line tools
------------------

Use ``./manage.py import_form <file.json>`` to import a survey definition.

Use ``./manage.py import_answers <file.json>`` to import a survey answers from json.

Use ``python contrib/scripts/merge_forms.py`` for one time merging of VLE and VL surveys.

Note
----

Hard-coded value used in ``aoasurveys/static/js/aoa.js`` line ``87`` to identify fields that have choices.
Please consider replacing this with a computed value.


Contacts
========

The project owner is Franz Daffner (franz.daffner at eaa.europa.eu)

Other people involved in this project are:

* Alex Eftimie (alex.eftimie at eaudeweb.ro)


Resources
=========

Hardware
--------
Minimum requirements:
 * 2048MB RAM
 * 2 CPU 1.8GHz or faster
 * 4GB hard disk space

Recommended:
 * 4096MB RAM
 * 4 CPU 2.4GHz or faster
 * 8GB hard disk space


Software
--------
Any recent Linux version, apache2, MySQL server, Python 2.7


Copyright and license
=====================

This project is free software; you can redistribute it and/or modify it under
the terms of the EUPL v1.1.

More details under `LICENSE.txt`_.

.. _`LICENSE.txt`: https://github.com/eaudeweb/aoa-surveys/blob/master/LICENSE.txt
