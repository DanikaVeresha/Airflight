from functools import partial
from random import random
from geopy import Nominatim
from haversine import haversine, Unit

forcedpoint = 'NY'
geolocator = Nominatim(user_agent="test")
location = geolocator.geocode(forcedpoint)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)

forcedpoint1 = 'Miami'
geolocator = Nominatim(user_agent="test")
location = geolocator.geocode(forcedpoint1)
alatitude1 = location.latitude
alongitude1 = location.longitude
print(alatitude1, alongitude1)


reverse = partial(geolocator.reverse, language="es")
print(reverse((latitude, longitude)))
print(reverse((alatitude1, alongitude1)))
print(reverse((alongitude1, alatitude1)))



