from flask_restful import Resource
from flask import jsonify
from flask import request
from bson.json_util import loads
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager

prefix = "/api/v1/drivers"

import logging
import sys

class Drivers(Resource):

    def get(self):
        logging.info('GET: %s', prefix)
        db = DataBaseManager()
        try:
            drivers = db.getFrom('drivers',{})
            for driver in drivers:
                driver["_id"] = str(driver["_id"])
            return llevameResponse.successResponse(drivers,200)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error getting Drivers', 400)
    
    def post(self):
        logging.info('POST: %s', prefix)
        db = DataBaseManager()
        driver = {}
        body = request.get_json()

        try:
            driverId = db.postTo('drivers',[body])
        
            if len(driverId) == 1:
                body['_id'] = str(body['_id'])
                return llevameResponse.successResponse(body,200)
            else:
                logging.error('POST: %s - Error inserting new driver', prefix)
                return llevameResponse.errorResponse('Error inserting Driver', 400)
        except:
            logging.error('POST: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error inserting Driver', 400)

class DriversIds(Resource):

    def get(self, driverId):
        logging.info('GET: %s/%s', prefix, driverId)
        db = DataBaseManager()
        try:
            driver = db.getFrom('drivers',{'_id':ObjectId(driverId)})
            if len(driver) == 1:
                driver = driver[0]
                driver['_id'] = driverId
                return llevameResponse.successResponse(driver,200)
            else:
                return llevameResponse.errorResponse('There is no driver', 400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error returning driver', 400)
    
    def put(self, driverId):
        logging.info('PUT: %s/%s', prefix, driverId)
        return 'PUT request on ' + prefix + '/' + str(driverId)
    
    def delete(self, driverId):
        logging.info('DELETE: %s/%s', prefix, driverId)
        return 'DELETE request on ' + prefix + '/' + str(driverId)

class DriversIdsProfile(Resource):

    def get(self, driverId):
        logging.info('GET: %s/%s', prefix, driverId)
        db = DataBaseManager()
        try:
            driver = db.getFrom('drivers',{'_id' : ObjectId(driverId)})
            if len(driver) == 1:
                driver = driver[0]
                driver['_id'] = driverId
                return llevameResponse.successResponse(driver,200)
            else:
                return llevameResponse.errorResponse('There is no Driver', 400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error returning Driver', 400)

    def patch(self, driverId):
        logging.info('PATCH: %s/%s', prefix, driverId)

        db = DataBaseManager()
        body = request.get_json()
        try:
            driverProfile = db.update('drivers',driverId,body)
            logging.info('Driver profile updated')
            return llevameResponse.successResponse(driverProfile,200)
        except:
            logging.error('PATCH: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error updating driver profile', 400)