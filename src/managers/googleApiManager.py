from .dataBaseManager import DataBaseManager
import googlemaps 

import logging

class GoogleApiManager:
	apiKey = "AIzaSyAoNmFQRC3xZ4KC8764zs76DtgTYBgzxfE"

	def getAddressForLocation(self, location):
		gmaps =  googlemaps.Client(key=self.apiKey)
		print((location['latitude'], location['longitude']))
		reverse = gmaps.reverse_geocode((location['latitude'], location['longitude']))
		if len(reverse) > 0:
			print(reverse[0]['formatted_address'])
			return reverse[0]['formatted_address']
		return None

	def getDirectionsForAddress(self, start, end):
		gmaps = googlemaps.Client(key=self.apiKey)
		directions  = gmaps.directions(start, end, alternatives=True)
		print(directions)
		roads = []
		for direction in directions:	# directions -> list of dictionaries
			road = []
			leg = direction['legs'][0] # just one leg because there is no waypoints
			road.append(leg['start_location'])
			for step in leg['steps']: 
				road.append(step['end_location'])

			roads.append(road)
			if len(roads) == 5: #limit to only 5 options max
				break

		return roads
