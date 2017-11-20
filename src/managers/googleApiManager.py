from .dataBaseManager import DataBaseManager
from googlemaps import GoogleMaps

import logging

class GoogleApiManager:
	apiKey = "AIzaSyAoNmFQRC3xZ4KC8764zs76DtgTYBgzxfE"

	def getAddressForLocation(self, location):
		gmaps = GoogleMaps(self.apiKey)
		reverse = gmaps.reverse_geocode(location['latitude'], location['longitude'])
		if 'Placemark' in reverse and len(reverse['Placemark']) > 0:
			return reverse['Placemark'][0]['address']
		return None

	def getDirectionsForAddress(self, start, end):
		gmaps = GoogleMaps(self.apiKey)
		directions  = gmaps.directions(start, end) 
		return directions['Directions']['Routes']
