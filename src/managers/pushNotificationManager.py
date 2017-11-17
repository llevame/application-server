from pyfcm import FCMNotification
from bson.objectid import ObjectId
from .dataBaseManager import DataBaseManager

import logging

class PushNotificationsManager:
	apiKey = "AAAA5nKlvbU:APA91bEIKGmva3-XnmTZmvFTEByh3haHxKO1yCfUy3kgBSo3_azbW88Q6Xu_lk4gj28T1ht0thVnKbq5HeFKGMKHV6xT7U9wy4RDNr2Y5hZ6vt4xog3mlE3NlbAydhMlNYLc6S0tmZ5u"


	def sendUserPush(self, userId):
		users = DataBaseManager().getFrom('users',{'_id':ObjectId(userId)})
		if len(users) == 1:
			user = users[0]
			if not 'deviceId' in user:
				logging.error("Push Notifications - user " + userId + " do not have device Id for push notifications")
				return

			deviceId = user['deviceId']
			return self.sendPush(deviceId)

		logging.error("Push Notifications - user not found")
		return None


	def sendDriverPush(self, userId):
		users = DataBaseManager().getFrom('drivers',{'_id':ObjectId(userId)})
		if len(users) == 1:
			user = users[0]
			if not 'deviceId' in user:
				logging.error("Push Notifications - driver " + userId + " do not have device Id for push notifications")
				return

			deviceId = user['deviceId']
			return self.sendPush(deviceId)
		logging.error("Push Notifications - driver not found")
		return None


	def sendPush(self, deviceID):
		push_service = FCMNotification(api_key=apiKey)

		registration_id = deviceID
		message_title = "message title"
		message_body = "message"
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		print(result)
		logging.info(result)
		return result

	def sendMultiplePush(self, deviceIDs):
		if not isinstance(deviceIDs,list):
			logging.error("Push Notifications - device ids is not a list")
			return

		push_service = FCMNotification(api_key=apiKey)

		registration_ids = deviceIDs
		message_title = "message title"
		message_body = "message"
		result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
		print(result)
		logging.info(result)
		return result
