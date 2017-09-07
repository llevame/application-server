from flask_restful import Resource

prefix = "/api/v1/trips"

class Trips(Resource):
    def post(self):
        return 'POST request on ' + prefix

class TripsEstimate(Resource):
    def post(self):
        return 'POST request on ' + prefix + '/estimate'

class TripsIds(Resource):
    def get(self, tripId):
        return 'GET request on ' + prefix + '/' + str(tripId)


