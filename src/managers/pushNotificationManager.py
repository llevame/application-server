from pyfcm import FCMNotification
from .dataBaseManager import DataBaseManager
from enum import IntEnum

import logging

class PushType(IntEnum):
    DEFAULT = 0
    NEW_TRIP = 1
    ACCEPTED_TRIP = 2
    FINISHED_TRIP = 3
    CANCELED_TRIP = 4


class PushNotificationManager:
	apiKey = "AAAA5nKlvbU:APA91bEIKGmva3-XnmTZmvFTEByh3haHxKO1yCfUy3kgBSo3_azbW88Q6Xu_lk4gj28T1ht0thVnKbq5HeFKGMKHV6xT7U9wy4RDNr2Y5hZ6vt4xog3mlE3NlbAydhMlNYLc6S0tmZ5u"

	def sendNewTripPush(self, username, tripId):
		dataMessage = {"tripId": tripId, "type":PushType.NEW_TRIP}
		self.sendDriverPush(username, title="New trip", body="New trip available", dataMessage=dataMessage)

	def sendTripAcceptedPush(self, username, tripId):
		dataMessage = {"tripId": tripId, "type":PushType.ACCEPTED_TRIP}
		self.sendUserPush(username, title="Trip accepted", body="Your driver will contact you", dataMessage=dataMessage)

	def sendTripCanceledPush(self, username, tripId):
		dataMessage = {"tripId": tripId, "type":PushType.CANCELED_TRIP}
		self.sendUserPush(username, title="Trip rejected", body="Your driver has rejected your trip, choose another one", dataMessage=dataMessage)

	def sendTripFinishedPush(self, username, tripId):
		dataMessage = {"tripId": tripId, "type":PushType.FINISHED_TRIP}
		self.sendUserPush(username, title="Trip finished", dataMessage=dataMessage)



	def sendUserPush(self, username, title = "title", body = "", dataMessage = None):
		users = DataBaseManager().getFrom('users',{'username':username})
		if len(users) == 1:
			user = users[0]
			if not 'firebaseToken' in user:
				logging.error("Push Notifications - user " + username + " do not have device Id for push notifications")
				return None

			deviceId = user['firebaseToken']
			return self.sendPush(deviceId, title=title, body=body, dataMessage=dataMessage)

		logging.error("Push Notifications - user not found")
		return None


	def sendDriverPush(self, username, title = "title", body = "", dataMessage = None):
		users = DataBaseManager().getFrom('drivers',{'username':username})
		if len(users) == 1:
			user = users[0]
			if not 'firebaseToken' in user:
				logging.error("Push Notifications - driver " + username + " do not have device Id for push notifications")
				return None

			deviceId = user['firebaseToken']
			return self.sendPush(deviceId, title=title, body=body, dataMessage=dataMessage)
		logging.error("Push Notifications - driver not found")
		return None


	def sendPush(self, deviceID, title = "Llevame App", body = "", dataMessage = None):
		push_service = FCMNotification(api_key= self.apiKey)

		result = push_service.notify_single_device(registration_id=deviceID, message_title=title, message_body=body, data_message=dataMessage)
		print(result)
		logging.info(result)
		return result

	def sendMultiplePush(self, deviceIDs):
		if not isinstance(deviceIDs,list):
			logging.error("Push Notifications - device ids is not a list")
			return None

		push_service = FCMNotification(api_key= self.apiKey)

		registration_ids = deviceIDs
		message_title = "message title"
		message_body = "message"
		result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
		print(result)
		logging.info(result)
		return result