from flask_restful import Resource
from flask import request
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager
from managers.authManager import Authorization
from managers.pushNotificationManager import PushNotificationManager
from managers.googleApiManager import GoogleApiManager

from enum import IntEnum
from threading import Timer

import time

import logging
import sys

class TripStatusEnum(IntEnum):
    CREATED = 0
    ASSIGNATED = 1
    IN_PROGRESS = 2
    FINISHED = 3
    CANCELED = 4

prefix = "/api/v1/trips"
auth = Authorization().auth

def cancelTrip(passenger, tripId):
    trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
    # If trip wasnt assignated yet, cancel it
    if len(trips) == 1 and (trips[0])['status'] == TripStatusEnum.CREATED:
        logging.info('Trip %s canceled after time out', tripId)
        DataBaseManager().update('trips', tripId,{'status': TripStatusEnum.CANCELED})
        PushNotificationManager().sendTripCanceledPush(passenger, tripId)



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
                body['status'] = TripStatusEnum.CREATED

                tripIds = db.postTo('trips',[body])
                tripId = str(tripIds[0])
                PushNotificationManager().sendNewTripPush(body['driver'], tripId)

                timer = Timer(1 * 60, cancelTrip, [user['username'], tripId])
                timer.start()

                responseData = {'tripId': tripId}
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


class TripTentative(Resource):
    def post(self):
        #TODO: integrate with shared to get estimated cost
        logging.info('POST: %s/tentative', prefix)
        try:
            body = request.get_json()
            if 'start' not in body or 'end' not in body:
                return llevameResponse.errorResponse('start and end point are mandatory', 403)

            if 'latitude' not in body['start'] or 'longitude' not in body['start']:
                return llevameResponse.errorResponse('start as {latitude: X, longitude: X} is mandatory', 403)
            if 'latitude' not in body['end'] or 'longitude' not in body['end']:
                return llevameResponse.errorResponse('end as {latitude: X, longitude: X} is mandatory', 403)

            startAddress = GoogleApiManager().getAddressForLocation(body['start'])
            if startAddress is None:
                logging.error('POST tentative trip - Invalid start')
                return llevameResponse.errorResponse('Invalid start point', 403)

            endAddress = GoogleApiManager().getAddressForLocation(body['end'])
            if endAddress is None:
                logging.error('POST tentative trip - Invalid end')
                return llevameResponse.errorResponse('Invalid end point', 403)

            directions = GoogleApiManager().getDirectionsForAddress(startAddress, endAddress)

            responseData = {'directions':directions, 'cost':0}
            return llevameResponse.successResponse(responseData, 200)
            
        except:
            logging.error('POST: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error creating tentative trip', 400)


class TripStatus(Resource):
    @auth.login_required
    def patch(self, tripId):
        logging.info('PATCH: %s/status', prefix)
        try:
            body = request.get_json()
            if 'status' not in body:
                return llevameResponse.errorResponse('status is mandatory', 401)

            newStatus = body['status']
            trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
            if len(trips) == 1:
                trip = trips[0]

                driver = Authorization().getDriverFrom(request)
                if driver is None or (trip['driver'] != driver['username']): 
                    logging.info('PATCH: %s/status - error: invalid user', prefix)
                    return llevameResponse.errorResponse('Invalid user', 403)

                actualStatus = trip['status']

                if actualStatus >= newStatus:
                    logging.info('PATCH: %s/status - actual status(%d) greater than new one(%d)', prefix, actualStatus, newStatus)
                    return llevameResponse.errorResponse('Invalid new status', 401)

                if newStatus == TripStatusEnum.ASSIGNATED and actualStatus == TripStatusEnum.CREATED:
                    DataBaseManager().update('trips', str(trip["_id"]),{'status':newStatus})
                    PushNotificationManager().sendTripAcceptedPush(trip["passenger"], tripId)
                    logging.info('PATCH: %s/status - trip assignated', prefix)
                    return llevameResponse.successResponse({'tripId':tripId},200)

                if newStatus == TripStatusEnum.IN_PROGRESS and actualStatus == TripStatusEnum.ASSIGNATED:
                    DataBaseManager().update('trips', str(trip["_id"]),{'status':newStatus})
                    logging.info('PATCH: %s/status - trip started', prefix)
                    return llevameResponse.successResponse({'tripId':tripId},200)

                if newStatus == TripStatusEnum.FINISHED and actualStatus == TripStatusEnum.IN_PROGRESS:
                    DataBaseManager().update('trips', str(trip["_id"]),{'status':newStatus})
                    PushNotificationManager().sendTripFinishedPush(trip["passenger"], tripId)
                    logging.info('PATCH: %s/status - trip finished', prefix)
                    return llevameResponse.successResponse({'tripId':tripId},200)

                if newStatus == TripStatusEnum.CANCELED:
                    # TODO: Define what to do if trip was in progress and was caneled
                    DataBaseManager().update('trips', str(trip["_id"]),{'status':newStatus})
                    PushNotificationManager().sendTripCanceledPush(trip["passenger"], tripId)
                    logging.info('PATCH: %s/status - trip canceled', prefix)
                    return llevameResponse.successResponse({'tripId':tripId},200)

                logging.info('PATCH: %s/status - invalid new status %d (actual status: %d)', prefix, newStatus, actualStatus)
                return llevameResponse.errorResponse("invalid new status",401)

            return llevameResponse.errorResponse("trip not found",400)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error starting trip', 400)


class TripsIds(Resource):
    """
    * Agrega una posicion al trip en progreso
    """	
    @auth.login_required
    def patch(self, tripId):
        logging.info('PATCH: %s/%s', prefix, tripId)
        try:
            body = request.get_json()
            if 'location' not in body:
                return llevameResponse.errorResponse('location is mandatory', 401)

            if 'latitude' not in body['location'] or 'longitude' not in body['location']:
                return llevameResponse.errorResponse('location as {latitude: X, longitude: X} is mandatory', 401)

            position = body['location']

            trips = DataBaseManager().getFrom('trips',{'_id':ObjectId(tripId)})
            if len(trips) == 1:
                trip = trips[0]

                if trip['status'] != TripStatusEnum.IN_PROGRESS:
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

