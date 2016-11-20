import rethinkdb as r
import semantic_version
import json
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
    def post(self, deployment_name):
        deployment = json.loads(request.data)

        deployments_table = "deployments"

        unique_ness = deployment['server'] + str(deployment['local_port'])
        unique_ness = unique_ness.lower()

        #make sure the incoming deployment name is unused
        r.connect(rethinkdb_host, rethinkdb_port).repl()
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, deployments_table)
        keys = r.db(rethinkdb_db).table(deployments_table).run()
        db_deployments = list(keys)

        for dep in db_deployments:
            db_uniqueness = dep['server'] + str(dep['local_port'])
            db_uniqueness = db_uniqueness.lower()
            if unique_ness == db_uniqueness:
                raise ValueError("Already exists")

        result = r.db(rethinkdb_db).table(deployments_table).insert(deployment).run()
        return result

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



    def put(self, deployment_id):
        deployment = json.loads(request.data)
        deployments_table = "deployments"
        r.connect(rethinkdb_host, rethinkdb_port).repl()
        db_deployment = r.db(rethinkdb_db).table(deployments_table).get(deployment_id).run()
        db_deployment['status'] = deployment['status']
        db_deployment['deployment_name'] = deployment['deployment_name']
        db_deployment['local_port'] = deployment['local_port']
        db_deployment['package_version'] = deployment['package_version']
        db_deployment['server'] = deployment['server']
        db_deployment['package_branch'] = deployment['package_branch']
        result = r.db(rethinkdb_db).table(deployments_table).get(deployment_id).replace(db_deployment).run()
        return result

    def delete(self, deployment_id):
        deployments_table = "deployments"
        r.connect(rethinkdb_host, rethinkdb_port).repl()
        db_deployment = r.db(rethinkdb_db).table(deployments_table).get(deployment_id).run()
        if db_deployment:
            result = r.db(rethinkdb_db).table(deployments_table).get(deployment_id).delete().run()
            return result



api.add_resource(ApiDeployment, '/api/deployments/', '/api/deployments/server/<string:server>/','/api/deployments/appmap/<string:appmap>/','/api/deployments/deployment/<string:deployment_id>/','/api/deployments/create/<string:deployment_name>/')
api.add_resource(ApiDeploymentServer, '/api/servers/')
