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
		return 'Default endpoint on ' + prefix
		
	def post(self):

		return jsonify(response)
