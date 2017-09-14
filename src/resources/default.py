from flask_restful import Resource
import logging

prefix = "/api/v1"

class Default(Resource):
    def get(self):
        logging.info('GET: %s', prefix)
        return 'Default endpoint on ' + prefix

