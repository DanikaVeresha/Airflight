from geopy import Nominatim
from haversine import haversine, Unit

forcedpoint = input('Enter the forced point: ')
geolocator = Nominatim(user_agent="test")
location = geolocator.geocode(forcedpoint)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)

forcedpoint1 = input('Enter the forced point: ')
geolocator = Nominatim(user_agent="test")
location = geolocator.geocode(forcedpoint1)
alatitude = location.latitude
alongitude = location.longitude
print(alatitude, alongitude)

distance = haversine((latitude, longitude), (alatitude, alongitude), unit=Unit.MILES)
a = distance
print(a)