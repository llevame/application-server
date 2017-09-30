from flask_restful import Resource
from flask import jsonify
from flask import request

prefix = "/api/v1/users"

import logging

class Drivers(Resource):

    def get(self):
        logging.info('GET: %s', prefix)
        return 'GET request on ' + prefix
    
    def post(self):
        logging.info('POST: %s', prefix)
        return 'POST request on ' + prefix

class DriversIds(Resource):

    def get(self, userId):
        logging.info('GET: %s/%s', prefix, userId)
        return 'GET request on ' + prefix + '/' + str(userId)
    
    def put(self, userId):
        logging.info('PUT: %s/%s', prefix, userId)
        return 'PUT request on ' + prefix + '/' + str(userId)
    
    def delete(self, userId):
        logging.info('DELETE: %s/%s', prefix, userId)
        return 'DELETE request on ' + prefix + '/' + str(userId)

class DriversIdsProfile(Resource):

    def get(self, userId):
        logging.info('GET: %s/%s', prefix, userId)
        driver = {'name' : 'Nicolas', "lastname" : 'Alvarez' , 'carId' : 2134123 , 'driverId' : userId}
        return jsonify(driver)

    def path(self, userId):
        logging.info('PATCH: %s/%s', prefix, userId)
        #Init mocked data for driver
        driver = {'name' : 'Nicolas', "lastname" : 'Alvarez' , 'carId' : 2134123 , 'driverId' : userId}
        #End mocked data for drive
        body = request.get_json()
        try:
            for key in body:
                if key in driver and key != 'driverId' :
                    driver[key] = body[key]
        except:
            logging.error('Error parsing JSON:' + body)
        return driver