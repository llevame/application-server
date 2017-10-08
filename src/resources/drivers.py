from flask_restful import Resource
from flask import jsonify
from flask import request

prefix = "/api/v1/drivers"

import logging

class Drivers(Resource):

    def get(self):
        logging.info('GET: %s', prefix)
        return 'GET request on ' + prefix
    
    def post(self):
        logging.info('POST: %s', prefix)
        return 'POST request on ' + prefix

class DriversIds(Resource):

    def get(self, driverId):
        logging.info('GET: %s/%s', prefix, driverId)
        return 'GET request on ' + prefix + '/' + str(driverId)
    
    def put(self, driverId):
        logging.info('PUT: %s/%s', prefix, driverId)
        return 'PUT request on ' + prefix + '/' + str(driverId)
    
    def delete(self, driverId):
        logging.info('DELETE: %s/%s', prefix, driverId)
        return 'DELETE request on ' + prefix + '/' + str(driverId)

class DriversIdsProfile(Resource):

    def get(self, driverId):
        logging.info('GET: %s/%s', prefix, driverId)
        driver = {'name' : 'Nicolas', "lastname" : 'Alvarez' , 'carId' : 2134123 , 'driverId' : driverId}
        return jsonify(driver)

    def patch(self, driverId):
        logging.info('PATCH: %s/%s', prefix, driverId)
        #Init mocked data for driver
        driver = {'name' : 'Nicolas', "lastname" : 'Alvarez' , 'carId' : 2134123 , 'driverId' : driverId}
        #End mocked data for drive
        body = request.get_json()
        try:
            for key in body:
                if key in driver and key != 'driverId' :
                    driver[key] = body[key]
        except:
            logging.error('Error parsing JSON:' + body)
        return driver