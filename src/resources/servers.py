from flask_restful import Resource
import logging

prefix = "/api/v1/servers"

class ServersPing(Resource):
    def post(self):
        logging.info('POST: %s/ping', prefix)
        return 'POST request on ' + prefix + '/ping'
