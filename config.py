"""
This module defines the environment variables that will be used to configure the flask application

basedir: absolute path to the directory including this module and the app module

SECRET_KEY: the secret key is accessed through an environment variable instead of being embedded in the code.This variable is used as a general-purpose encryption key by Flask and several third-party extensions. Hence choose a very hard string to remember to replace the default 'hard to guess string'

SQLALCHEMY_DATABASE_URI:  database is specified as a URI.
i.e. 
dbengine://username:password@hostname/database
- dbengine is the database engine to use among mysql, postgresql or sqlite.
- hostname refers to the server that hosts the MySQL service
- username and password are used for authentification
- database refers to the name of the database

SQLite databases do not have a server, but are simple files, so hostname, username, and password are omitted and database is the filename of a disk file: e.g.
'sqlite:///' + os.path.join(basedir, 'data.sqlite')'
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv("SECRET_KEY") or "hard to guess string"

# To use a postgres db hosted on a postgres server, set the following env vars and USE_POSTGRES to any non-falsy values (e.g. 1)
password = os.getenv("POSTGRES_PASSWORD")
username = os.getenv("POSTGRES_USER")
database = os.getenv("POSTGRES_DB")
hostname = "db"
if os.getenv("USE_POSTGRES"):
	# use a psotgres db using above env variables
	SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@{hostname}/{database}"
else:
	# simply use a SQLlite database (<=> flat file)
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
    	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
