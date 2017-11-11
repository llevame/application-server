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

class AccountMe(Resource):
    @auth.login_required
    def get(self):
        logging.info('GET: %s/me', prefix)
        db = DataBaseManager()
        try:
            user = Authorization().getUserFrom(request)
            if user is None:
                user = Authorization().getDriverFrom(request)

            if user is None:
                return llevameResponse.errorResponse('Invalid user', 403)

            user.pop('_id')
            return llevameResponse.successResponse(user,200)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error getting Users', 400)

    @auth.login_required
    def patch(self):
        logging.info('PATCH: %s/me', prefix)
        db = DataBaseManager()
        body = request.get_json()
        try:
            collection = 'users'
            user = Authorization().getUserFrom(request)
            if user is None:
                collection = 'drivers'
                user = Authorization().getDriverFrom(request)

            if user is None:
                return llevameResponse.errorResponse('Invalid user', 403)

            userProfile = db.update(collection, str(user["_id"]),body)
            logging.info('User profile updated' + str(body))
            return llevameResponse.successResponse({},200)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error updating user profile', 400)


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
		return (Serializer(AppKey, 3600).dumps({'username': username})).decode("utf-8") 

	# Login user -> updates token
	def patch(self, username):
		body = request.json
		logging.info('PATCH: %s/%s - body: %s', prefix, username, str(body))
		try:
			user = DataBaseManager().getFrom('users',{'username':username})
			if len(user) == 1:
				return self.loginPassenger(user[0], body)

			user = DataBaseManager().getFrom('drivers',{'username':username})
			if len(user) == 1:
				return self.loginDriver(user[0], body)

			return llevameResponse.errorResponse('Error finding User', 401)

		except:
			error = 'PATCH' + str(sys.exc_info()[0]) + "-" + str(sys.exc_info()[1])
			logging.error(error)
			return llevameResponse.errorResponse(error, 400)


	def loginPassenger(self, user, body):
		if 'password' in user:
			# Regular user
			hashPass = user['password']
			if not 'password' in body:
				logging.error('login user: password not found')
				return llevameResponse.errorResponse('Wrong password', 401)

			password = body['password']

			if self.verifyPass(hashPass, password):
				# Refresh token for user
				newToken = Account().getToken(user['username'])
				DataBaseManager().update('users', str(user["_id"]), {'token': newToken})

				dataResponse = {'token': newToken, 'isDriver': False}
				return llevameResponse.successResponse(dataResponse,200)
			return llevameResponse.errorResponse('Wrong password', 401)

		elif 'fb_token' in user and 'fb_token' in body:
			# Facebook user
			if user['fb_token'] == body['fb_token']:			
				newToken = Account().getToken(user['username'])
				DataBaseManager().update('users', str(user["_id"]), {'token': newToken})

				dataResponse = {'token': newToken, 'isDriver': False}
				return llevameResponse.successResponse(dataResponse,200)
			return llevameResponse.errorResponse('Invalid facebook token', 401)

		return llevameResponse.errorResponse('Error finding User. Needs password or fb token', 400)


	def loginDriver(self, user, body):
		if 'password' in user:
			hashPass = user['password']
			if not 'password' in body:
				logging.error('login user: password not found')
				return llevameResponse.errorResponse('Wrong password', 401)

			password = body['password']

			if self.verifyPass(hashPass, password):
				# Refresh token for user
				newToken = Account().getToken(user['username'])
				DataBaseManager().update('drivers', str(user["_id"]), {'token': newToken})

				dataResponse = {'token': newToken, 'isDriver': True}
				return llevameResponse.successResponse(dataResponse,200)
			return llevameResponse.errorResponse('Wrong password', 401)

		return llevameResponse.errorResponse('Error finding User. Needs password', 500)


	# Sign up user
	def post(self, username):
		body = request.json
		logging.info('POST: %s/%s - body: %s', prefix, username, str(body))
		try:
			if not ('isDriver' in body):
				logging.error('Sign up user: invalid driver info')
				return llevameResponse.errorResponse('isDriver is mandatory', 203)

			isDriver = body['isDriver']
			if isDriver:
				return self.signUpDriver(username, body)
			else:
				return self.signUpPassenger(username, body)

		except:
			error = 'POST' + str(sys.exc_info()[0]) + "-" + str(sys.exc_info()[1])
			logging.error(error)
			return llevameResponse.errorResponse(error, 400)


	def signUpPassenger(self, username, body):
		user = DataBaseManager().getFrom('users',{'username':username})
		if len(user) >= 1:
			logging.error('POST %s - %s : User already exists')
			return llevameResponse.errorResponse('User already exists', 401)

		if 'password' in body and len(body['password']):
			return self.signUpRegularUser(username, body)
		if 'fb_token' in body and len(body['fb_token']):
			return self.signUpFacebookUser(username, body)

		logging.error('Sign up user: invalid password')
		return llevameResponse.errorResponse('password or fb_token is mandatory', 203)


	def signUpRegularUser(self, username, body):
		password = body['password']
		hashPass = self.getHashPassword(password)
		if self.verifyPass(hashPass, password):
			token = Account().getToken(username)
			body['token'] = token
			body['username'] = username
			body['password'] = hashPass

			userId = DataBaseManager().postTo('users',[body])
			if len(userId) > 0:
				logging.info('POST: %s/%s - user created', prefix, username)
				dataResponse = {'token': token, 'isDriver': False}
				return llevameResponse.successResponse(dataResponse,200)
			else:
				logging.error('Sign up user: cant post new user %s', username)
				return llevameResponse.errorResponse('Internal error', 500)
		
		logging.error('Sign up user: cant get pass from hash')
		return llevameResponse.errorResponse('Internal error', 500)


	def signUpFacebookUser(self, username, body):
		token = Account().getToken(username)
		body['token'] = token
		body['username'] = username
		userId = DataBaseManager().postTo('users',[body])
		
		if len(userId) > 0:
			logging.info('POST: %s/%s - user created', prefix, username)
			dataResponse = {'token': token, 'isDriver': False}
			return llevameResponse.successResponse(dataResponse,200)

		logging.error('Sign up user: cant post new user %s', username)
		return llevameResponse.errorResponse('Internal error', 500)


	def signUpDriver(self, username, body):
		user = DataBaseManager().getFrom('drivers',{'username':username})
		if len(user) >= 1:
			logging.error('POST %s - %s : User already exists')
			return llevameResponse.errorResponse('User already exists', 401)

		if (not 'password' in body) or (len(body['password']) == 0):
			logging.error('Sign up user: invalid password')
			return llevameResponse.errorResponse('Password is mandatory', 203)

		password = body['password']
		hashPass = self.getHashPassword(password)
		if self.verifyPass(hashPass, password):
			token = Account().getToken(username)
			body['token'] = token
			body['username'] = username
			body['password'] = hashPass

			userId = DataBaseManager().postTo('drivers',[body])
			if len(userId) > 0:
				logging.info('POST: %s/%s - driver created', prefix, username)
				dataResponse = {'token': token, 'isDriver': True}
				return llevameResponse.successResponse(dataResponse,200)
			else:
				logging.error('Sign up user: cant post new user %s', username)
				return llevameResponse.errorResponse('Internal error', 500)
		else:
			logging.error('Sign up user: cant get pass from hash')
			return llevameResponse.errorResponse('Internal error', 500)

