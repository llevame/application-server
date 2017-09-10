from flask_restful import Resource
import logging

prefix = "/api/v1/users"



class Users(Resource):
    def get(self):
        logging.info('GET: %s', prefix)
        return 'GET request on ' + prefix
    def post(self):
        logging.info('POST: %s', prefix)
        return 'POST request on ' + prefix

class UsersValidate(Resource):
    def post(self):
        logging.info('POST: %s/validate', prefix)
        return 'POST request on ' + prefix + '/validate'

class UsersIds(Resource):
    def get(self, userId):
        logging.info('GET: %s/%s', prefix, userId)
        return 'GET request on ' + prefix + '/' + str(userId)
    def put(self, userId):
        logging.info('PUT: %s/%s', prefix, userId)
        return 'PUT request on ' + prefix + '/' + str(userId)
    def delete(self, userId):
        logging.info('DELETE: %s/%s', prefix, userId)
        return 'DELETE request on ' + prefix + '/' + str(userId)

class UsersIdsCars(Resource):
    def get(self, userId):
        logging.info('GET: %s/%s/cars', prefix, userId)
        return 'GET request on ' + prefix + '/' + str(userId) + '/cars'
    def post(self, userId):
        logging.info('POST: %s/%s/cars', prefix, userId)
        return 'POST request on ' + prefix + '/' +  str(userId) + '/cars'

class UsersIdsCarsIds(Resource):
    def get(self, userId, carId):
        logging.info('GET: %s/%s/cars/%s', prefix, userId, carId)
        return 'GET request on ' + prefix + '/' +  str(userId) + '/cars/' + str(carId)
    def put(self, userId, carId):
        logging.info('PUT: %s/%s/cars/%s', prefix, userId, carId)
        return 'PUT request on ' + prefix + '/' +  str(userId) + '/cars/' + str(carId)

    def delete(self, userId, carId):
        logging.info('DELETE: %s/%s/cars/%s', prefix, userId, carId)
        return 'DELETE request on ' + prefix + '/' +  str(userId) + '/cars/' + str(carId)

class UsersIdsTransactions(Resource):
    def get(self, userId):
        logging.info('GET: %s/%s/transactions', prefix, userId)
        return 'GET request on ' + prefix + '/' +  str(userId) + '/transactions'
    def post(self, userId):
        logging.info('POST: %s/%s/transactions', prefix, userId)
        return 'POST request on ' + prefix + '/' +  str(userId) + '/transactions'

