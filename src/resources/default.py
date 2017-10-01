from flask_restful import Resource
from flask import request
from flask import jsonify
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
		
	def post(self):
		client = MongoClient('mongodb://localhost:27017/')
		dataBase = client.project # Name of the data base
		driverCollection = dataBase["drivers"]
		body = request.get_json()
		driverId = driverCollection.insert_one(body).inserted_id
		response = {'driverId' : str(driverId), 'name' : body['name'] , 'lastname' : body['lastname'] , 'description' : body['description']}
		return jsonify(response)
