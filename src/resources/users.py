from flask_restful import Resource

prefix = "/api/v1"

class Users(Resource):
    def get(self):
        return 'GET request on ' + prefix + '/users'
    def post(self):
        return 'POST request on ' + prefix + '/users'

class UsersIds(Resource):
    def get(self, userId):
        return 'GET request on ' + prefix + '/users/' + userId
