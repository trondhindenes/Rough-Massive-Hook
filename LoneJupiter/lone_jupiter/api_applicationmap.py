import rethinkdb as r
import semantic_version
from flask_restful import Resource, Api, request, fields, marshal_with
from lone_jupiter import app, appconfig, api
from helpers.rethinkdb_helper import RethinkDbHelper

rethinkdb_host = appconfig['rethinkdb_host']
rethinkdb_port = appconfig['rethinkdb_port']
rethinkdb_db = appconfig['rethinkdb_db']


class ApiDeploymentMap(Resource):
    def get(self):

        appmaps_table = "applicationmaps"

        r.connect(rethinkdb_host, rethinkdb_port).repl()
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, appmaps_table)
        keys = r.db(rethinkdb_db).table(appmaps_table).run()
        db_appmaps = list(keys)
        return db_appmaps


api.add_resource(ApiDeploymentMap, '/api/applicationmaps/')
