from flask_restful import Resource

prefix = "/api/v1/users/"

class Users(Resource):
    def get(self):
        return 'GET request on ' + prefix
    def post(self):
        return 'POST request on ' + prefix

class UsersValidate(Resource):
    def post(self):
        return 'POST request on ' + prefix + '/validate'

class UsersIds(Resource):
    def get(self, userId):
        return 'GET request on ' + prefix + str(userId)
    def put(self, userId):
        return 'PUT request on ' + prefix + str(userId)
    def delete(self, userId):
        return 'DELETE request on ' + prefix + str(userId)

class UsersIdsCars(Resource):
    def get(self, userId):
        return 'GET request on' + prefix + str(userId)+ 'cars'
    def post(self, userId):
        return 'POST request on' + prefix + str(userId)+ 'cars'

class UsersIdsCarsIds(Resource):
    def get(self, userId, carId):
        return 'GET request on ' + prefix + str(userId) + '/cars/' + str(carId)
    def put(self, userId, carId):
        return 'PUT request on ' + prefix + str(userId) + '/cars/' + str(carId)

    def delete(self, userId, carId):
        return 'DELETE request on ' + prefix + str(userId) + '/cars/' + str(carId)

class UsersIdsTransactions(Resource):
    def get(self, userId):
        return 'GET request on ' + prefix + str(userId) + '/transactions'
    def post(self, userId):
        return 'POST request on ' + prefix + str(userId) + '/transactions'

