from managers.dataBaseManager import DataBaseManager
from flask_httpauth import HTTPTokenAuth

import logging

# TODO: Use another secret key
AppKey = "asdasdadsasdasd"

class Authorization:
	auth = HTTPTokenAuth()

	@auth.verify_token
	def verifyToken(token):
		logging.info('verify token: %s', token)
		db = DataBaseManager()
		user = db.getFrom('users',{'token':token})
		if len(user) == 1:
			logging.info('User found ' + token)
			return True

		user = db.getFrom('drivers',{'token':token})
		if len(user) == 1:
			logging.info('Driver found ' + token)
			return True

		logging.info('User not found')
		return False

	@staticmethod
	def getUserFrom(request):
		auth_header = request.headers.get('Authorization')
		token = auth_header.split(" ")[1]

		user = DataBaseManager().getFrom('users',{'token':token})
		if len(user) == 1:
			return user[0]
		return None

	@staticmethod
	def getDriverFrom(request):
		auth_header = request.headers.get('Authorization')
		token = auth_header.split(" ")[1]

		user = DataBaseManager().getFrom('drivers',{'token':token})
		if len(user) == 1:
			return user[0]
		return None
