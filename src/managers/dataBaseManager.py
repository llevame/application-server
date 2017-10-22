from pymongo import MongoClient
from pymongo import errors
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads

import logging


# WIP: DataBaseManager singleton
class DataBaseManager(object):
	__instance = None
	# client = MongoClient('mongodb://localhost:27017/')

	client = MongoClient('mongodb://dymloz:twinkltwinkl1@ds117605.mlab.com:17605/heroku_nlvr8zs7')

	dataBase = client.heroku_nlvr8zs7 # Name of the data base

	def __new__(cls):
		if DataBaseManager.__instance is None:
			DataBaseManager.__instance = object.__new__(cls)
		return DataBaseManager.__instance

	# Get objects from collection with 'collectionName', matching properties on 'matching'
	# collectionName: String. Name of the collection.
	# matching: Dictionary with keys as properties on collection and values as wished
	def getFrom(self, collectionName, matching):
		try:
			collection = self.dataBase[collectionName]
			matches = collection.find(matching)
			logging.info("Getting document successfully")
			return loads(dumps(matches))
		except errors.CollectionInvalid as e:
			logging.error('GET error: invalid collection')
			return {}
		except errors.OperationFailure as e:
			logging.error('GET error: %s', e.details)
			return {}

	# Post 'objects' to collection with 'collectionName'
	# collectionName: String. Name of the collection.
	# objects: Dictionary with keys as properties on collection and values as wished
	def postTo(self, collectionName, objects):
		try:
			collection = self.dataBase[collectionName]
			result = collection.insert_many(objects)
			logging.info("Document insertion dsuccessfull")
			return result.inserted_ids
		except errors.CollectionInvalid as e:
			logging.error('POST error: invalid collection')
			return {}
		except errors.OperationFailure as e:
			logging.error('POST error: %s', e.details)
			return {}

	# Update object with 'docId' to collection with 'collectionName' with 'uptadeData'
	# collectionName: String. Name of the collection.
	# objects: Dictionary with keys as properties on collection and values as wished
	def update(self, collectionName, docId, updateData):
		try:
			collection = self.dataBase[collectionName]
			result = collection.update_one({'_id': ObjectId(docId)}, {"$set": updateData}, upsert=False)
			logging.info("Document updated successfully")
			return result.upserted_id
		except errors.CollectionInvalid as e:
			logging.error('UPDATE error: invalid collection')
			return {}
		except errors.OperationFailure as e:
			logging.error('UPDATE error: %s', e.details)
			return {}
