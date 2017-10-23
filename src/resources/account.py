from flask_restful import Resource
from flask import jsonify
from flask_restful import Resource
from flask import jsonify
from flask import request
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager

from passlib.hash import sha256_crypt

import logging
import sys

prefix = "/api/v1/account"

class Account(Resource):
    def getHashPassword(self, password):
        return sha256_crypt.encrypt(password)

    def verifyPassword(self, hashPass, password):
        return sha256_crypt.verify(password, hashPass)

    def put(self, username, password):
    	return llevameResponse.successResponse({"username":"nicolas", "password":"1234"}, 200)

    # Sign up user
    def post(self, username, password):
    	logging.info('POST: %s/%s/%s', prefix, username, password)
    	db = DataBaseManager()
    	body = request.get_json()
    	try:
    		user = db.getFrom('users',{'username':username})
    		if len(user) >= 1:
    			return llevameResponse.errorResponse('User already exists', 400)
    		else:
    			hashPass = self.getHashPassword(password)
    			if self.verifyPassword(hashPass, password):
    				body['username'] = username
    				body['password'] = hashPass
    				userId = db.postTo('users',[body])
    				if len(userId) > 0:
    					user = db.getFrom('users',{'_id':userId})
    					dataResponse = {'token': '1234', 'user': user}
    					return llevameResponse.successResponse(dataResponse,200)
    				else:
    					logging.error('Sign up user: cant post new user %s', username)
    					return llevameResponse.errorResponse('Internal error', 500)
    			else:
    				logging.error('Sign up user: cant get pass from hash')
    				return llevameResponse.errorResponse('Internal error', 500)
    	except:
    		logging.error('POST: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
    		return llevameResponse.errorResponse('Error Sign Up User', 400)


    # Login user with password
    def get(self, username, password):
        logging.info('GET: %s/%s/%s', prefix, username, password)
        db = DataBaseManager()
        try:
            user = db.getFrom('users',{'username':username})
            if len(user) == 1:
                user = user[0]
                user["_id"] = str(user["_id"])
                hashPass = user['password']
                user.pop('password') 	# Remove key from response
                if self.verifyPassword(hashPass, password):
                	db.update('users', user['_id'], {'token': '1234'})
                	dataResponse = {'token': '1234', 'user': user}

                	return llevameResponse.successResponse(dataResponse,200)

                return llevameResponse.errorResponse('Invalid password', 401)
            else:
                return llevameResponse.errorResponse('Error finding User', 400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error Login User', 400)

