from flask import Flask
from flask_restful import Resource, Api

from resources.default import Default

from resources.account import Account

from resources.users import Users
from resources.users import UsersValidate
from resources.users import UsersIds
from resources.users import UsersIdsProfile
from resources.users import UsersIdsCars
from resources.users import UsersIdsCarsIds
from resources.users import UsersIdsTransactions

from resources.drivers import Drivers
from resources.drivers import DriversIds
from resources.drivers import DriversIdsProfile
from resources.trips import Trips
from resources.trips import TripsEstimate
from resources.trips import TripsIds
from managers.apiConfig import ApiConfig

from resources.paymethods import Paymethods

from resources.servers import ServersPing

import logging
import os
import requests

app = Flask(__name__)
api = Api(app)
SHARED_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MCwicm9sZXMiOlsiYWRtaW4iXSwiaWF0IjoxNTA5OTM2MjA1LCJleHAiOjE1MTAxMDg4NDJ9.kkn0BtV-icJsE1Dj4EGGi3ktkPkQtFVeFqBt-jTufxU"

API_TOKEN = ""

prefix = "/api/v1"

# logs
if not os.path.exists("../logs"):
    os.makedirs("../logs")
appConfig = ApiConfig()
# Getting shared token
applicationParams = {
	'username' : "dymloz",
	'password' : "dymloz91"
}
applicationUserRequest = requests.post(url = appConfig.SHARED_URL + '/api/token', data = applicationParams)
if applicationUserRequest.status_code == 201:
	data = applicationUserRequest.json()
	appConfig.SHARED_TOKEN = data["token"]["token"]

	params = {'token' : appConfig.SHARED_TOKEN}
	r = requests.post(url = appConfig.SHARED_URL + '/api/servers/1', params = params)
	if r.status_code == 201:
		data = r.json()
		appConfig.API_TOKEN = data["server"]["token"]["token"]
		logging.info('Success getting shared token')
		print "Success getting shared token"
	else:
		logging.error('Error authentication with shared')
		print "Error authentication with shared"
else:
	print applicationUserRequest.json()
	logging.error('Error getting token for shared')
	print "Error getting token for shared"


log = open("../logs/appServer.log", "w")
log.close()

logging.basicConfig(filename='../logs/appServer.log', format='%(asctime)s , %(levelname)s : %(message)s' ,  level=logging.INFO)

# Default endpoint
api.add_resource(Default, prefix)

# Account endpoints
api.add_resource(Account, '{}/account/<string:username>'.format(prefix))

# Users endpoints
api.add_resource(Users, '{}/users'.format(prefix))
api.add_resource(UsersValidate, '{}/users/validate'.format(prefix))
api.add_resource(UsersIds, '{}/users/<string:userId>'.format(prefix))
api.add_resource(UsersIdsProfile, '{}/users/<string:userId>/profile'.format(prefix))
api.add_resource(UsersIdsCars, '{}/users/<int:userId>/cars'.format(prefix))
api.add_resource(UsersIdsCarsIds, '{}/users/<int:userId>/cars/<int:carId>'.format(prefix))
api.add_resource(UsersIdsTransactions, '{}/users/<int:userId>/transactions'.format(prefix))

# Trips endpoints
api.add_resource(Trips, '{}/trips'.format(prefix))
api.add_resource(TripsEstimate, '{}/trips/estimate'.format(prefix))
api.add_resource(TripsIds, '{}/trips/<int:tripId>'.format(prefix))

# Drivers endpoints
api.add_resource(Drivers, '{}/drivers'.format(prefix))
api.add_resource(DriversIds, '{}/drivers/<string:driverId>'.format(prefix))
api.add_resource(DriversIdsProfile, '{}/drivers/<string:driverId>/profile'.format(prefix))

# Paymethods endpoints
api.add_resource(Paymethods, '{}/paymethods'.format(prefix))

# Servers endpoints
api.add_resource(ServersPing, '{}/servers/ping'.format(prefix))

if __name__ == "__main__":
    app.run(debug=True)

