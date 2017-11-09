from flask_restful import Resource
from flask import jsonify
from flask import request
from managers.apiConfig import ApiConfig
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager
from managers import sharedServices
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from managers.authManager import Authorization

import logging
import sys

prefix = "/api/v1/account"
auth = Authorization().auth
apiConfig = ApiConfig()

AppKey = "asdasdadsasdasd"

class Account(Resource):
    
	def getHashPassword(self, password):
		return sha256_crypt.encrypt(password)

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

	@auth.login_required
	def put(self, username):
		return llevameResponse.successResponse({"username":"nicolas", "password":"1234"}, 200)

	# Login user
	def get(self, username):
		logging.info('GET: %s/%s', prefix, username)
		db = DataBaseManager()
		body = request.get_json()
		try:
			user = db.getFrom('users',{'username':username})
			if len(user) == 1:
				user = user[0]
				hashPass = user['password']
				password = body['password']

				if self.verifyPass(hashPass, password):
					# Refresh token for user
					newToken = Account().getToken(user['username'])
					db.update('users', str(user["_id"]), {'token': newToken})

					dataResponse = {'token': newToken}
					return llevameResponse.successResponse(dataResponse,200)

				return llevameResponse.errorResponse('Invalid password', 401)
			else:
				return llevameResponse.errorResponse('Error finding User', 400)
		except:
			logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
			return llevameResponse.errorResponse('Error Login User', 400)

	# Sign up user
	def post(self, username):
		logging.info('POST: %s/%s', prefix, username)
		db = DataBaseManager()
		body = request.get_json()
		sharedResponse = sharedServices.postToShared(apiConfig.SHARED_URL + '/api/users', body, {})
		print sharedResponse
		try:
			user = db.getFrom('users',{'username':username})
			if len(user) >= 1:
				return llevameResponse.errorResponse('User already exists', 400)
			else:
				password = body['password']
				if password.len() == 0:
					logging.error('Sign up user: invalid password %s', password)
					return llevameResponse.errorResponse('Invalid password', 203)

				hashPass = self.getHashPassword(password)
				if self.verifyPass(hashPass, password):
					body['token'] = Account().getToken(username)
					body['username'] = username
					body['password'] = hashPass
					userId = db.postTo('users',[body])
					if len(userId) > 0:
						dataResponse = {'token': body['token']}
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
