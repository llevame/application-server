from flask_restful import Resource
from pymongo import MongoClient
from pymongo import errors
from bson.json_util import dumps
import logging

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from managers.dataBaseManager import DataBaseManager

prefix = "/api/v1"

class Default(Resource):
    def get(self):	
		client = MongoClient('mongodb://localhost:27017/')
		dataBase = client.project # Name of the data base
		collection = dataBase["collectionName"]
		matches = collection.find({"a":1})
		return dumps(matches)

		#return DataBaseManager().getFrom("asd",{"a":1})

		logging.info('GET: %s', prefix)
		return 'Default endpoint on ' + prefix