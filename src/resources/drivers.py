from flask_restful import Resource
from flask import jsonify
from flask import request
from bson.json_util import loads
from managers import sharedServices
from bson.objectid import ObjectId
from . import llevameResponse
from managers.dataBaseManager import DataBaseManager
from managers.authManager import Authorization

import logging
import sys


prefix = "/api/v1/drivers"
auth = Authorization().auth


def makeUserSecure(user):
    user.pop("_id", None)
    user.pop("password", None)
    user.pop("token", None)
    user.pop("fb_token", None)

class Drivers(Resource):
    @auth.login_required
    def get(self):
        logging.info('GET: %s', prefix)
        db = DataBaseManager()
        try:
            users = db.getFrom('drivers',{})
            for user in users:
                makeUserSecure(user)
            return llevameResponse.successResponse(users,200)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error getting Drivers', 400)

class DriversProfile(Resource):
    @auth.login_required
    def get(self, driverId):
        logging.info('GET: %s/%s/profile', prefix, driverId)
        db = DataBaseManager()
        try:
            driver = db.getFrom('drivers',{'username':driverId})
            if len(driver) == 1:
                driver = driver[0]
                sharedResponse = sharedServices.getToShared("/api/users/" + str(driver["sharedId"]), {})
                if sharedResponse["success"] == True:
                    userShared = sharedResponse["data"]["user"]
                    userShared.pop('id')
                    userShared.pop('_ref')
                    userShared.pop('applicationOwner')
                    userShared.update(driver)
                    user = userShared
                else:
                    loggin.error('Error getting user from shared server')
                makeUserSecure(driver)
                return llevameResponse.successResponse(driver,200)
            else:
                return llevameResponse.errorResponse('There is no driver', 400)
        except:
            logging.error('GET: %s - %s', sys.exc_info()[0],sys.exc_info()[1])
            return llevameResponse.errorResponse('Error returning driver', 400)