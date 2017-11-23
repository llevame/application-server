from .dataBaseManager import DataBaseManager
import googlemaps 

import logging

class GoogleApiManager:
	apiKey = "AIzaSyAoNmFQRC3xZ4KC8764zs76DtgTYBgzxfE"

	def getAddressForLocation(self, location):
		gmaps =  googlemaps.Client(key=self.apiKey)
		reverse = gmaps.reverse_geocode((location['latitude'], location['longitude']))
		if len(reverse) > 0:
			return reverse[0]['formatted_address']
		return None

	def getDirectionsForAddress(self, start, end):
		gmaps = googlemaps.Client(key=self.apiKey)
		directions  = gmaps.directions(start, end, alternatives=True)
		roads = []
		for direction in directions:	# directions -> list of dictionaries
			road = []
			leg = direction['legs'][0] # just one leg because there is no waypoints

			startLocation = leg['start_location'] 
			road.append({"latitude": startLocation["lat"], "longitude": startLocation["lng"]})

			for step in leg['steps']: 
				location = step['end_location']
				road.append({"latitude": location["lat"], "longitude": location["lng"]})

			roads.append(road)
			if len(roads) == 5: #limit to only 5 options max
				break

		return roads
