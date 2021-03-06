import rethinkdb as r
from flask_restful import Resource, Api, request
from lone_jupiter import app, appconfig, api, reqparse
from helpers.rethinkdb_helper import RethinkDbHelper
from models.Artifact import Artifact

rethinkdb_host = appconfig['rethinkdb_host']
rethinkdb_port = appconfig['rethinkdb_port']
rethinkdb_db = appconfig['rethinkdb_db']

artifact_fields = Artifact.artifact_fields

class ApiArtifact(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('commit_id', type=str, location='json')
        self.reqparse.add_argument('package_name', type=str, location='json')
        self.reqparse.add_argument('package_version', type=str, location='json')
        self.reqparse.add_argument('branch_name', type=str, location='json')
        self.reqparse.add_argument('commit_author', type=str, location='json')
        self.reqparse.add_argument('commit_message', type=str, location='json')
        self.reqparse.add_argument('artifact_url', type=str, location='json')
        self.reqparse.add_argument('package_name', type=str, location='json')
        self.reqparse.add_argument('artifact_type', type=str, location='json')
        super(ApiArtifact, self).__init__()

        r.connect(rethinkdb_host, rethinkdb_port).repl()


    def get(self):

        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, "artifacts")

        keys = r.db(rethinkdb_db).table("artifacts").run()
        db_artifacts = list(keys)
        artifacts = []
        for af in db_artifacts:
            artifacts.append(af)
        return artifacts


    def post(self):
        artifact = request.get_json(force=True)
        RethinkDbHelper.ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, "artifacts")
        try:
            insert_obj = {
                "commit_id": artifact['commit_id'],
                "package_name": artifact['package_name'],
                "package_version": artifact['package_version'],
                "branch_name": artifact['branch_name'],
                "commit_author": artifact['commit_author'],
                "commit_message": artifact['commit_message'],
                "commit_tag": artifact['commit_tag'],
                "artifact_url": artifact['artifact_url'],
                "artifact_type": artifact['artifact_type']
            }

            existing_record = \
                r.db(rethinkdb_db).table("artifacts").filter({'commit_id': artifact['commit_id'],
                        'package_name': artifact['package_name'], 'package_version': artifact['package_version']}).run()

            if existing_record.items.__len__() == 0:
                result = r.db(rethinkdb_db).table("artifacts").insert(insert_obj).run();
            elif existing_record.items.__len__() == 1:

                insert_obj['id'] = existing_record.items[0]['id']
                result = r.db(rethinkdb_db).table("artifacts").insert(insert_obj, conflict="replace").run();
            return result
        except Exception, e:
            raise ValueError(str.format("error {0}", str(e)))



api.add_resource(ApiArtifact, '/api/release')


