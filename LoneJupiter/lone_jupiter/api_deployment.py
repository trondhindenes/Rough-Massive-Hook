import rethinkdb as r
import semantic_version
from flask_restful import Resource, Api, request, fields, marshal_with
from lone_jupiter import app, appconfig, api
from helpers.rethinkdb_helper import RethinkDbHelper

rethinkdb_host = appconfig['rethinkdb_host']
rethinkdb_port = appconfig['rethinkdb_port']
rethinkdb_db = appconfig['rethinkdb_db']


class ApiDeploymentServer(Resource):
    def get(self):

        servers_table = "servers"

        r.connect(rethinkdb_host, rethinkdb_port).repl()
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, servers_table)
        keys = r.db(rethinkdb_db).table(servers_table).run()
        db_servers = list(keys)
        return db_servers

class ApiDeployment(Resource):
    def get(self, server=None, appmap=None):

        deployments_table = "deployments"

        r.connect(rethinkdb_host, rethinkdb_port).repl()
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, deployments_table)
        keys = r.db(rethinkdb_db).table(deployments_table).run()
        db_deployments = list(keys)
        if server:
            db_deployments = [x for x in db_deployments if x['server'] == server]

        if appmap:
            db_deployments = [x for x in db_deployments if x['deployment_name'] == appmap]
        return db_deployments


api.add_resource(ApiDeployment, '/api/deployments/', '/api/deployments/server/<string:server>','/api/deployments/appmap/<string:appmap>')
api.add_resource(ApiDeploymentServer, '/api/servers/')
