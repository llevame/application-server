from flask_restful import Resource

prefix = "/api/v1/paymethods"

class Paymethods(Resource):
    def get(self):
        return 'GET request on ' + prefix

