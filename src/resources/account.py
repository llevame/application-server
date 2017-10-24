from flask_restful import Resource
from flask import jsonify
from flask import request
#from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth

from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager

from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import logging
import sys

prefix = "/api/v1/account"
#auth = HTTPBasicAuth()
auth = HTTPTokenAuth()

AppKey = "asdasdadsasdasd"

class Account(Resource):
    
	def getHashPassword(self, password):
		return sha256_crypt.encrypt(password)

	#    @auth.verify_password
	def verifyPassword(username, password):
		logging.info('verify password: %s/%s', username, password)
		db = DataBaseManager()
		user = db.getFrom('users',{'username':username})
		if len(user) == 1:
			logging.info('User found')
			user = user[0]

			if Account().verifyPass(user['password'], password):
				logging.info('correct pass')
				return True
		logging.info('User not found')
		return False

	def verifyPass(self, hashPass, password):
		return sha256_crypt.verify(password, hashPass)

	def getToken(self, username):
		return Serializer(AppKey, 3600).dumps({'username': username})

	@auth.verify_token
	def verifyToken(token):
		logging.info('verify token: %s', token)
		db = DataBaseManager()
		user = db.getFrom('users',{'token':token})
		print(user)
		if len(user) == 1:
			logging.info('User found')
			return True

		logging.info('User not found')
		return False

	@auth.login_required
	def put(self, username, password):
		return llevameResponse.successResponse({"username":"nicolas", "password":"1234"}, 200)

	# Login user with password
	def get(self, username, password):
		logging.info('GET: %s/%s/%s', prefix, username, password)
		db = DataBaseManager()
		try:
			user = db.getFrom('users',{'username':username})
			if len(user) == 1:
				user = user[0]
				# Refresh token for user
				newToken = Account().getToken(user['username'])
				db.update('users', user['_id'], {'token': newToken})

				user["_id"] = str(user["_id"])
				user["token"] = newToken

				hashPass = user['password']
				user.pop('password') 	# Remove key from response

				if self.verifyPass(hashPass, password):
					dataResponse = {'user': user}
					return llevameResponse.successResponse(dataResponse,200)

				return llevameResponse.errorResponse('Invalid password', 401)
			else:
				return llevameResponse.errorResponse('Error finding User', 400)
		except:
			logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
			return llevameResponse.errorResponse('Error Login User', 400)

	# Sign up user
	def post(self, username, password):
		logging.info('POST: %s/%s/%s', prefix, username)
		db = DataBaseManager()
		body = request.get_json()
		try:
			user = db.getFrom('users',{'username':username})
			if len(user) >= 1:
				return llevameResponse.errorResponse('User already exists', 400)
			else:
				passw = body['password']
				if passw.len() == 0:
					logging.error('Sign up user: invalid password %s', passw)
					return llevameResponse.errorResponse('Invalid password', 203)

				hashPass = self.getHashPassword(passw)
				if self.verifyPass(hashPass, passw):
					body['token'] = Account().getToken(username)
					body['username'] = username
					body['password'] = hashPass
					userId = db.postTo('users',[body])
					if len(userId) > 0:
						user = db.getFrom('users',{'_id':userId})
						user.pop('password') 	# Remove key from response
						dataResponse = {'user': user}
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
