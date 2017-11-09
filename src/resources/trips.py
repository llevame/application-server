from flask_restful import Resource
from flask import request
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager
from managers.authManager import Authorization

#from enum import Enum

import time

import logging
import sys

#class TripStatus(Enum):
CREATED = 0
IN_PROGRESS = 1
FINISHED = 2
CANCELED = 3

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
                body['status'] = CREATED

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

class TripInProgress(Resource):
    @auth.login_required
    def patch(self, tripId):
        logging.info('PATCH: %s/start', prefix)
        try:
            trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
            if len(trips) == 1:
                trip = trips[0]

                if trip['status'] != CREATED:
                    return llevameResponse.errorResponse('This trip cant be started again', 401)

                driver = Authorization().getDriverFrom(request)
                if driver is None or (trip['driver'] != driver['username']): 
                    logging.info('PATCH: %s/start - error: invalid user', prefix)
                    return llevameResponse.errorResponse('Invalid user', 403)

                tripId = DataBaseManager().update('trips', str(trip["_id"]),{'status':IN_PROGRESS})
                return llevameResponse.successResponse({'tripId':tripId},200)

            return llevameResponse.errorResponse("trip not found",400)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error starting trip', 400)


class TripFinished(Resource):
    @auth.login_required
    def patch(self, tripId):
        logging.info('PATCH: %s/end', prefix)
        try:
            trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
            if len(trips) == 1:
                trip = trips[0]

                if trip['status'] != IN_PROGRESS:
                    return llevameResponse.errorResponse('This trip cant be finished because it isnt started', 401)

                driver = Authorization().getDriverFrom(request)
                if driver is None or (trip['driver'] != driver['username']): 
                    logging.info('PATCH: %s/start - error: invalid user', prefix)
                    return llevameResponse.errorResponse('Invalid user', 403)

                tripId = DataBaseManager().update('trips', str(trip["_id"]),{'status':FINISHED})
                return llevameResponse.successResponse({'tripId':tripId},200)


            return llevameResponse.errorResponse("trip not found",400)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error ending trip', 400)

class TripsIds(Resource):
    """
    * Agrega una posicion al trip en progreso
    """	
    @auth.login_required
    def patch(self, tripId):
        logging.info('PATCH: %s/%s', prefix, tripId)
        try:
            body = request.get_json()
            if 'position' not in body:
                return llevameResponse.errorResponse('position is mandatory', 401)

            if 'lat' not in body['position'] or 'lon' not in body['position']:
                return llevameResponse.errorResponse('position as {lat: X, lon: X} is mandatory', 401)

            position = body['position']

            trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
            if len(trips) == 1:
                trip = trips[0]

                if trip['status'] != IN_PROGRESS:
                    return llevameResponse.errorResponse('This trip cant be edited because it isnt started', 401)

                passenger = Authorization().getUserFrom(request)
                driver = Authorization().getDriverFrom(request)
                if passenger is None and driver is None:
                    return llevameResponse.errorResponse('Invalid user', 403)

                if passenger is None and trip['driver'] == driver['username']:
                    return self.updateTripPostion(trip, driver, position)

                if driver is None and trip['passenger'] == passenger['username']:
                    return self.updateTripPostion(trip, passenger, position)

                return llevameResponse.errorResponse('Invalid user', 403)

            return llevameResponse.errorResponse("trip not found",400)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error updating trip', 400)

    def updateTripPostion(self, trip, user, position):
        logging.info('PATCH: %s/%s - Update passenger postion', prefix, str(trip["_id"]))
        roadTripKey = 'road.' + user['username']
        updateQuery = {"$push": {roadTripKey: position}}
        print(updateQuery)
        tripId = DataBaseManager().updateWith('trips', str(trip["_id"]),updateQuery)
        return llevameResponse.successResponse({'tripId':str(trip["_id"])},200)



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

