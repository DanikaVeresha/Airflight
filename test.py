from geopy import Nominatim

forcedpoint = input('Enter the forced point: ')
geolocator = Nominatim(user_agent="test")
location = geolocator.geocode(forcedpoint)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)
