from flask_restful import Resource
import logging

prefix = "/api/v1/paymethods"

class Paymethods(Resource):
    def get(self):
        logging.info('GET: %s', prefix)
        return 'GET request on ' + prefix

