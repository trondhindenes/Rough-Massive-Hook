import os
from ConfigParser import SafeConfigParser
from flask import Flask
from flask_restful import Resource, Api, reqparse, fields


app = Flask(__name__)

cwd = os.getcwd()
#current dir
here = os.path.dirname(__file__)
#parent dir
parent = os.path.abspath(os.path.join(here, os.pardir))

config_file_path = os.path.join(parent, 'config.ini')
if os.path.isfile(config_file_path) is False:
    raise ValueError(str.format("unable to find file {0}", config_file_path))
config = SafeConfigParser()

try:
    config.read(config_file_path)
    appconfig = {}
    appconfig['rethinkdb_host'] = config.get("Default", "rethinkdb_host")
    appconfig['rethinkdb_port'] = config.get("Default", "rethinkdb_port")
    appconfig['rethinkdb_db'] = config.get("Default", "rethinkdb_db")
except Exception, e:
    raise ValueError(str.format("error reading ini file {0}: {1}", config_file_path), str(e))

api = Api(app)
import lone_jupiter.api_artifact

