from flask import Flask
from flask_restful import Resource, Api

from resources.default import Default

from resources.users import Users
from resources.users import UsersValidate
from resources.users import UsersIds
from resources.users import UsersIdsCars
from resources.users import UsersIdsCarsIds
from resources.users import UsersIdsTransactions

from resources.trips import Trips
from resources.trips import TripsEstimate
from resources.trips import TripsIds

from resources.paymethods import Paymethods

from resources.servers import ServersPing

import logging

app = Flask(__name__)
api = Api(app)

prefix = "/api/v1"

# Default endpoint
logging.basicConfig(filename='../logs/appServer.log', format='%(asctime)s , %(levelname)s : %(message)s' ,  level=logging.INFO)

api.add_resource(Default, prefix)

# Users endpoints
api.add_resource(Users, '{}/users'.format(prefix))
api.add_resource(UsersValidate, '{}/users/validate'.format(prefix))
api.add_resource(UsersIds, '{}/users/<int:userId>'.format(prefix))
api.add_resource(UsersIdsCars, '{}/users/<int:userId>/cars'.format(prefix))
api.add_resource(UsersIdsCarsIds, '{}/users/<int:userId>/cars/<int:carId>'.format(prefix))
api.add_resource(UsersIdsTransactions, '{}/users/<int:userId>/transactions'.format(prefix))

# Trips endpoints
api.add_resource(Trips, '{}/trips'.format(prefix))
api.add_resource(TripsEstimate, '{}/trips/estimate'.format(prefix))
api.add_resource(TripsIds, '{}/trips/<int:tripId>'.format(prefix))

# Paymethods endpoints

api.add_resource(Paymethods, '{}/paymethods'.format(prefix))

# Servers endpoints

api.add_resource(ServersPing, '{}/servers/ping'.format(prefix))

if __name__ == "__main__":
    app.run(debug=True)

