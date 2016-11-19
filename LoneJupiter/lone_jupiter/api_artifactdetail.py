import rethinkdb as r
import semantic_version
from flask_restful import Resource, Api, request
from lone_jupiter import app, appconfig, api
from helpers.rethinkdb_helper import RethinkDbHelper

rethinkdb_host = appconfig['rethinkdb_host']
rethinkdb_port = appconfig['rethinkdb_port']
rethinkdb_db = appconfig['rethinkdb_db']

class ApiArtifactDetail(Resource):
    def get(self, name, branch="any", version="latest", ):

        r.connect(rethinkdb_host, rethinkdb_port).repl()
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, "artifacts")

        if version == 'latest' and branch == 'any':
            existing_record = \
                r.db(rethinkdb_db).table("artifacts").filter({'package_name': name}).run()

            all_records = existing_record.items
            current_highest = None
            for rec in all_records:
                try:
                    v = semantic_version.Version(rec['package_version'])
                except:
                    v = semantic_version.Version('0.0.0')
                rec['semantic_version'] = v
                if current_highest is None:
                    current_highest = rec
                else:
                    this_wins = current_highest['semantic_version'] < v
                    if this_wins:
                        rec['semantic_version'] = v
                        current_highest = rec
            #remove the semantic version from the object before returning, since it's not json serializable
            del current_highest['semantic_version']
            return current_highest



        elif version == 'latest': #we need to query for branch since it was specified
            existing_record = \
                r.db(rethinkdb_db).table("artifacts").filter({'package_name': name, 'branch_name': branch}).run()
            recordset = []
            for item in existing_record.items:
                recordset.append(item)

            if recordset.__len__() == 1:
                return recordset[0]





        return None

api.add_resource(ApiArtifactDetail, '/api/artifactdetail/<string:name>/<string:branch>/<string:version>')