import rethinkdb as r
import semantic_version
from flask_restful import Resource, Api, request, fields, marshal_with
from lone_jupiter import app, appconfig, api
from helpers.rethinkdb_helper import RethinkDbHelper
from helpers.server_selector import ServerSelector
import requests
import json

rethinkdb_host = appconfig['rethinkdb_host']
rethinkdb_port = appconfig['rethinkdb_port']
rethinkdb_db = appconfig['rethinkdb_db']
serverpool_port_start = appconfig['serverpool_port_start']


class ApiDeploymentSelector(Resource):
    def get(self, appmap_name):

        appmaps_table = "applicationmaps"

        r.connect(rethinkdb_host, rethinkdb_port).repl()
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, appmaps_table)

        keys = r.db(rethinkdb_db).table(appmaps_table).run()
        db_appmaps = list(keys)

        if db_appmaps.__len__() == 0:
            #not found
            pass
        if db_appmaps.__len__() < 1:
            #too many
            pass

        appmap = db_appmaps[0]
        desired_instancecount = appmap['instancecount']

        #figure out the existing number of deployments
        url = request.url_root + "api/deployments/appmap/" + appmap_name
        result = requests.get(url)
        result_data = json.loads(result.content)

        current_deployments = [x for x in result_data if x['package_version'] == appmap['gitfilter']['version'] and x['package_branch'] == appmap['gitfilter']['branch']]

        current_deployments_count = current_deployments.__len__()

        resultobj = {}
        resultobj['current_deployments'] = current_deployments_count
        resultobj['desired_deployments'] = desired_instancecount

        deployment_candidates = []
        if current_deployments_count < desired_instancecount:
            needed_deployments = desired_instancecount - current_deployments_count
            deployment_candidates = ServerSelector.get_deployment_candidates(rethinkdb_host, rethinkdb_port,
                                                                             rethinkdb_db, appmap['targettags'],
                                                                             needed_deployments, current_deployments)

            for candidate in deployment_candidates:
                port = ServerSelector.get_free_port(candidate['name'], request.url_root, serverpool_port_start)
                candidate['port'] = port
                result = ServerSelector.create_reservation(candidate, appmap, request.url_root)


        return deployment_candidates


api.add_resource(ApiDeploymentSelector, '/api/deploymentselector/<string:appmap_name>')
