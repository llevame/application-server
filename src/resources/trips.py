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
    * Debe estar la info driver (username) y viaje solicitado (array de posiciones)
    """	
    @auth.login_required
    def post(self):
        logging.info('POST: %s', prefix)
        db = DataBaseManager()
        body = request.get_json()

        try:
            user = Authorization().getUserFrom(request)
            if user is None:
                return llevameResponse.errorResponse('Invalid user', 403)

            if 'driver' not in body:
                return llevameResponse.errorResponse('driver is mandatory', 203)

            if ('trip' not in body) or (not isinstance(body['trip'], list)) or (len(body['trip']) == 0):
                return llevameResponse.errorResponse('trip as array is mandatory', 203)

            drivers = db.getFrom('drivers',{'username':body['driver']})
            if len(drivers) == 1:
                body = {'driver':body['driver'], 'passenger': user['username'], 'trip': body['trip'], 'time':time.time()}
                tripIds = db.postTo('trips',[body])
                responseData = {'tripId': str(tripIds[0])}
                return llevameResponse.successResponse(responseData,200)
            
            return llevameResponse.errorResponse('There is no driver', 201)
        except:
            logging.error('POST: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error saving trip for driver', 400)

    """
    * Retorna todos los viajes disponibles del driver que hace la consulta
    """	
    @auth.login_required
    def get(self):
        logging.info('GET: %s', prefix)
        db = DataBaseManager()

        try:
            driver = Authorization().getDriverFrom(request)
            if driver is None:
                return llevameResponse.errorResponse('Invalid user', 403)

            trips = db.getFrom('trips',{'driver':driver['username']})
            for trip in trips:
                trip['_id'] = str(trip['_id'])
            return llevameResponse.successResponse(trips,200)            

        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error getting trips for driver', 400)


class TripsEstimate(Resource):
    def post(self):
        logging.info('POST: %s/estimate', prefix)
        return 'POST request on ' + prefix + '/estimate'

class TripsIds(Resource):
    """
    * Retorna el viaje solicitado solo si quien lo pide es pasajero o driver del mismo
    """	
    @auth.login_required
    def get(self, tripId):
        logging.info('GET: %s/%s', prefix, tripId)
        try:
            trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
            if len(trips) == 1:
                trip = trips[0]
                trip['_id'] = str(trip['_id'])

                passenger = Authorization().getUserFrom(request)
                driver = Authorization().getDriverFrom(request)
                if passenger is None and driver is None:
                    return llevameResponse.errorResponse('Invalid user', 403)

                if passenger is None and trip['driver'] == driver['username']:
                    return llevameResponse.successResponse(trip,200)            

                if driver is None and trip['passenger'] == passenger['username']:
                    return llevameResponse.successResponse(trip,200)            

            return llevameResponse.errorResponse("trip not found",400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error getting trip', 400)

