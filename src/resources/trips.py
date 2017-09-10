from flask_restful import Resource
import logging

prefix = "/api/v1/trips"

class Trips(Resource):
    def post(self):
    	logging.info('POST: %s', prefix)
        return 'POST request on ' + prefix

class TripsEstimate(Resource):
    def post(self):
    	logging.info('POST: %s/estimate', prefix)
        return 'POST request on ' + prefix + '/estimate'

class TripsIds(Resource):
    def get(self, tripId):
    	logging.info('GET: %s/%s', prefix, tripId)
        return 'GET request on ' + prefix + '/' + str(tripId)


