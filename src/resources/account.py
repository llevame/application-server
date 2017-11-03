from flask_restful import Resource
from flask import jsonify
from flask import request

from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager

from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from managers.authManager import Authorization

import logging
import sys

prefix = "/api/v1/account"
auth = Authorization().auth

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

	# Login user -> updates token
	def patch(self, username):
		body = request.json
		logging.info('PATCH: %s/%s - body: %s', prefix, username, str(body))
		db = DataBaseManager()
		try:
			user = db.getFrom('users',{'username':username})
			if len(user) == 1:
				user = user[0]
				if len(user['password']) > 0:
					# Regular user
					hashPass = user['password']
					password = body['password']

					if self.verifyPass(hashPass, password):
						# Refresh token for user
						newToken = Account().getToken(user['username'])
						isDriver = user['isDriver']
						db.update('users', str(user["_id"]), {'token': newToken})

						dataResponse = {'token': newToken, 'isDriver': isDriver}
						return llevameResponse.successResponse(dataResponse,200)
					return llevameResponse.errorResponse('Invalid password', 401)

				elif len(user['token']) > 0:
					# Facebook user
					newToken = Account().getToken(user['username'])
					isDriver = user['isDriver']
					db.update('users', str(user["_id"]), {'token': newToken, 'isDriver':isDriver})

					dataResponse = {'token': newToken, 'isDriver': isDriver}
					return llevameResponse.successResponse(dataResponse,200)

				return llevameResponse.errorResponse('Error finding User. Needs password or fb token', 400)
			else:
				return llevameResponse.errorResponse('Error finding User', 400)
		except:
			logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
			return llevameResponse.errorResponse('Error Login User', 400)

	# Sign up user
	def post(self, username):
		body = request.json
		logging.info('POST: %s/%s - body: %s', prefix, username, str(body))
		db = DataBaseManager()
		try:
			user = db.getFrom('users',{'username':username})
			if len(user) >= 1:
				logging.error('POST %s - %s : User already exists')
				return llevameResponse.errorResponse('User already exists', 400)
			else:
				if (not body['password']) or (len(body['password']) == 0):
					logging.error('Sign up user: invalid password')
					return llevameResponse.errorResponse('Password is mandatory', 203)
				if not body['isDriver']:
					logging.error('Sign up user: invalid driver info')
					return llevameResponse.errorResponse('isDriver is mandatory', 203)

				password = body['password']
				hashPass = self.getHashPassword(password)
				if self.verifyPass(hashPass, password):
					body['token'] = Account().getToken(username)
					body['username'] = username
					body['password'] = hashPass
					userId = db.postTo('users',[body])
					if len(userId) > 0:
						logging.info('POST: %s/%s - user created', prefix, username)
						dataResponse = {'token': body['token'], 'isDriver':body['isDriver']}
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
