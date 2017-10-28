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
			logging.info('User found')
			return True

		logging.info('User not found')
		return False


