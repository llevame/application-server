from flask_restful import Resource
from flask import request
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager
from managers.authManager import Authorization

import time

import logging
import sys


prefix = "/api/v1/trips"
auth = Authorization().auth

class Trips(Resource):
    """
    * Guarda un viaje solicitado de un usuario a un driver especifico
    * Debe estar la info del usuario (username) y viaje solicitado (array de posiciones)
    """	
    @auth.login_required
    def post(self, driver):
        logging.info('POST: %s/%s', prefix, driver)
        db = DataBaseManager()
        body = request.get_json()

        try:
            if 'username' not in body:
                return llevameResponse.errorResponse('username is mandatory', 203)

            if ('trip' not in body) or (not isinstance(body['trip'], list)) or (len(body['trip']) == 0):
                return llevameResponse.errorResponse('trip as array is mandatory', 203)

            user = db.getFrom('users',{'username':body['username']})
            if len(user) != 1:
                return llevameResponse.errorResponse('There is no passenger', 201)

            drivers = db.getFrom('drivers',{'username':driver})
            if len(drivers) == 1:
                body = {'driver':driver, 'passenger': body['username'], 'trip': body['trip'], 'time':time.time()}
                tripIds = db.postTo('trips',[body])
                responseData = {'tripId': str(tripIds[0])}
                return llevameResponse.successResponse(responseData,200)
            
            return llevameResponse.errorResponse('There is no driver', 201)
        except:
            logging.error('POST: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error saving trip for driver', 400)

class TripsEstimate(Resource):
    def post(self):
        logging.info('POST: %s/estimate', prefix)
        return 'POST request on ' + prefix + '/estimate'

class TripsIds(Resource):
    def get(self, tripId):
        logging.info('GET: %s/trip/%s', prefix, tripId)
        return 'GET request on ' + prefix + '/' + str(tripId)


