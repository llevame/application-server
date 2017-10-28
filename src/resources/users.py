from flask_restful import Resource
from flask import jsonify
from flask import request
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager
from managers.authManager import Authorization


import logging
import sys

prefix = "/api/v1/users"
auth = Authorization().auth

class Users(Resource):

    @auth.login_required
    def get(self):
        logging.info('GET: %s', prefix)
        db = DataBaseManager()
        try:
            users = db.getFrom('users',{})
            for user in users:
                user["_id"] = str(user["_id"])
            return llevameResponse.successResponse(users,200)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error getting Users', 400)
    
    def post(self):
        logging.info('POST: %s', prefix)
        db = DataBaseManager()
        user = {}
        body = request.get_json()

        try:
            userId = db.postTo('users',[body])
        
            if len(userId) == 1:
                body['_id'] = str(body['_id'])
                return llevameResponse.successResponse(body,200)
            else:
                logging.error('POST: %s - Error inserting new user', prefix)
                return llevameResponse.errorResponse('Error inserting User', 400)
        except:
            logging.error('POST: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error inserting User', 400)

class UsersValidate(Resource):
    def post(self):
        logging.info('POST: %s/validate', prefix)
        return 'POST request on ' + prefix + '/validate'

class UsersIds(Resource):

    def get(self, userId):
        logging.info('GET: %s/%s', prefix, userId)
        db = DataBaseManager()
        try:
            user = db.getFrom('users',{'_id':ObjectId(userId)})
            if len(user) == 1:
                user = user[0]
                user['_id'] = userId
                return llevameResponse.successResponse(user,200)
            else:
                return llevameResponse.errorResponse('Error finding User', 400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error finding User', 400)
    def put(self, userId):
        logging.info('PUT: %s/%s', prefix, userId)
        return 'PUT request on ' + prefix + '/' + str(userId)
    
    def delete(self, userId):
        logging.info('DELETE: %s/%s', prefix, userId)
        return 'DELETE request on ' + prefix + '/' + str(userId)

class UsersIdsProfile(Resource):

    def get(self, userId):
        logging.info('GET: %s/%s', prefix, userId)
        db = DataBaseManager()
        try:
            user = db.getFrom('users',{'_id' : ObjectId(userId)})
            if len(user) == 1:
                user = user[0]
                user['_id'] = userId
                return llevameResponse.successResponse(user,200)
            else:
                return llevameResponse.errorResponse('Error finding User', 400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error finding User', 400)

    def patch(self, userId):
        logging.info('PATCH: %s/%s', prefix, userId)
        db = DataBaseManager()
        body = request.get_json()
        try:
            userProfile = db.update('users',userId,body)
            logging.info('User profile updated')
            return llevameResponse.successResponse(userProfile,200)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error updating user profile', 400)



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

