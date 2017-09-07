from flask_restful import Resource

prefix = "/api/v1"

class Default(Resource):
    def get(self):
        return 'Default endpoint on ' + prefix

