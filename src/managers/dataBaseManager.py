from pymongo import MongoClient
from pymongo import errors
from bson.json_util import dumps


# WIP: DataBaseManager singleton
class DataBaseManager(object):
	__instance = None
	client = MongoClient('mongodb://localhost:27017/')
	dataBase = client.project # Name of the data base

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
			return dumps(matches)
		except errors.CollectionInvalid as e:
			print "GET error: invalid collection"
			return {}
		except errors.OperationFailure as e:
			print "GET error: " + e.errno + " " + e.strerror
			return {}

	# Post 'objects' to collection with 'collectionName'
	# collectionName: String. Name of the collection.
	# objects: Dictionary with keys as properties on collection and values as wished
	def postTo(self, collectionName, objects):
		try:
			collection = self.dataBase[collectionName]
			result = collection.insert_many(objects)
			
			return result.inserted_ids
		except errors.CollectionInvalid as e:
			print "GET error: invalid collection"
			return {}
		except errors.OperationFailure as e:
			print "GET error: " + e.errno + " " + e.strerror
			return {}


# WIP: DataBaseManager as abstract class 
class asd(object):
	client = MongoClient('mongodb://localhost:27017/')
	dataBase = client.project # Name of the data base

	@classmethod
	# Get objects from collection with 'collectionName', matching properties on 'matching'
	# collectionName: String. Name of the collection.
	# matching: Dictionary with keys as properties on collection and values as wished
	def getFrom(cls, collectionName, matching):
		try:
			collection = cls.dataBase[collectionName]
			matches = collection.find(matching)
			return dumps(matches)
		except errors.CollectionInvalid as e:
			print "GET error: invalid collection"
			return {}
		except errors.OperationFailure as e:
			print "GET error: " + e.errno + " " + e.strerror
			return {}

	@classmethod
	# Post 'objects' to collection with 'collectionName'
	# collectionName: String. Name of the collection.
	# objects: Dictionary with keys as properties on collection and values as wished
	def postTo(cls, collectionName, objects):
		try:
			collection = cls.dataBase[collectionName]
			result = collection.insert_many(objects)
			
			return result.inserted_ids
		except errors.CollectionInvalid as e:
			print "GET error: invalid collection"
			return {}
		except errors.OperationFailure as e:
			print "GET error: " + e.errno + " " + e.strerror
			return {}
