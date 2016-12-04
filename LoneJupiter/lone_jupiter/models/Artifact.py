from flask_restful import fields

class Artifact(object):
    artifact_fields = {
        'commit_id': fields.String,
        'package_name': fields.String,
        'package_version': fields.String,
        'branch_name': fields.String,
        'commit_author': fields.String,
        'commit_message': fields.String,
        'commit_tag': fields.String,
        'artifact_url': fields.Url,
        'artifact_type': fields.String
    }
