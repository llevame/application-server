
class ApiConfig(object):
	__instance = None
	# client = MongoClient('mongodb://localhost:27017/')

	API_TOKEN = ""
	SHARED_TOKEN = ""
	SHARED_URL = "https://llevame-sharedserver.herokuapp.com"

	def __new__(cls):
		if ApiConfig.__instance is None:
			ApiConfig.__instance = object.__new__(cls)
		return ApiConfig.__instance