from managers.apiConfig import ApiConfig
import requests
import json

def postToShared(url,body,data):
	apiConfig = ApiConfig()

	print body

	data["token"] = apiConfig.API_TOKEN
	r = requests.post(url = url, data = body, params = json.dumps(data))
	if r.status_code == 401:
		params = {'token' : apiConfig.SHARED_TOKEN}
		r2 = requests.post(url = apiConfig.SHARED_URL + '/api/servers/1', params = params)
		if r2.status_code == 201:
			newTokenData = r2.json()
			apiConfig.API_TOKEN = newTokenData["server"]["token"]["token"]
			data["token"] = apiConfig.API_TOKEN
		else:
			print r2.status_code
			return {"success" : False, "data": r2.json(), "error": "Error al renovar el token"}

		r = requests.post(url = url, data = body, params = data)
	if r.status_code < 400:
		return {"success" : True , "data" : r.json()}
	else:
		return {"success" : False, "data": r.json(), "error": "Error al traer la info del shared"}

def getToShared(url,data):
	apiConfig = ApiConfig()
	data["token"] = apiConfig.API_TOKEN
	r = requests.get(url = url, params = data)
	if r.status_code == 401:
		params = {'token' : apiConfig.SHARED_TOKEN}
		r2 = requests.post(url = apiConfig.SHARED_URL + '/api/servers/1', params = params)
		if r2.status_code == requests.codes.ok:
			newTokenData = r2.json()
			apiConfig.API_TOKEN = newTokenData["server"]["token"]["token"]
			data["token"] = apiConfig.API_TOKEN
		else:
			return {"success" : False, "data": r2.json(), "error": "Error al renovar el token"}

		r = requests.post(url = url, data = body, params = data)
	if r.status_code < 400:
		return {"success" : True , "data" : r.json()}
	else:
		return {"success" : False, "data": r.json(), "error": "Error al traer la info del shared"}
	return
