from geopy.geocoders import Nominatim


class IIWBGeopy():

	def __init__(self) -> None:
		pass
	
	def get_coordinates(self, city):
		geolocator = Nominatim(user_agent="my_app")  # Replace "my_app" with your own user agent
		location = geolocator.geocode(city)
		if location is not None:
			latitude = location.latitude
			longitude = location.longitude
			return latitude, longitude
		else:
			return None
