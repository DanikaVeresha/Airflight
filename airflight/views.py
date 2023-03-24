import datetime
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from django.shortcuts import render, redirect
from airflight.models import AirLines, AirCompany, DeparturePoint, ArrivalPoint, UserList, ForcedPoint


def flight_launch(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    user_id = request.user.id
    pilot_list = UserList.objects.filter(id=user_id).first()
    if request.method == 'POST':
        aircommpany = request.POST.get('aircommpany')
        aircommpany_object = AirCompany(AirCommpany=aircommpany,
                                        AirFlight_id=pilot_list.AirFlight_id)
        aircommpany_object.save()
        departurepoint = request.POST.get('adress_airoport')
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departurepoint)
        departure_latitude = location.latitude
        departure_longitude = location.longitude
        departurepoint_object = DeparturePoint(DeparturePoint_name=departurepoint,
                                               DeparturePoint_latitude=departure_latitude,
                                               DeparturePoint_longitude=departure_longitude,
                                               AirFlight_id=pilot_list.AirFlight_id)
        departurepoint_object.save()
        arrivalpoint = request.POST.get('adress_airoporte')
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departurepoint)
        arrival_latitude = location.latitude
        arrival_longitude = location.longitude
        arrivalpoint_object = ArrivalPoint(ArrivalPoint_name=arrivalpoint,
                                           ArrivalPoint_latitude=arrival_latitude,
                                           ArrivalPoint_longitude=arrival_longitude,
                                           AirFlight_id=pilot_list.AirFlight_id)
        arrivalpoint_object.save()
        forcedpoint = ((departure_latitude + 1, departure_longitude - 1))
        location = geolocator.reverse(forcedpoint)
        forcedpoint_object = ForcedPoint(ForcedPoint_name=location.address,
                                         ForcedPoint_latitude=forcedpoint[0],
                                         ForcedPoint_longitude=forcedpoint[1],
                                         AirFlight_id=pilot_list.AirFlight_id)
        forcedpoint_object.save()
        airlines_object = AirLines(AirCommpany=aircommpany_object.AirCommpany,
                                   DeparturePoint=departurepoint_object.DeparturePoint_name,
                                   ArrivalPoint=arrivalpoint_object.ArrivalPoint_name,
                                   AirFlight_id=pilot_list.AirFlight_id,
                                   AirFlight_departure_date=datetime.datetime.now(),
                                   ForcedPoint=forcedpoint_object.ForcedPoint_name,
                                   AirFlight_status='Changed',
                                   Weather='Not favorable',
                                   Description_weather='Thunderstorm or no-fly zone')
        departure = airlines_object.DeparturePoint
        arrival = airlines_object.ArrivalPoint
        forced = airlines_object.ForcedPoint
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departure)
        departure_latitude = location.latitude
        departure_longitude = location.longitude
        location = geolocator.geocode(arrival)
        arrival_latitude = location.latitude
        arrival_longitude = location.longitude
        location = geolocator.geocode(forced)
        forced_latitude = location.latitude
        forced_longitude = location.longitude
        distancedf = haversine((departure_latitude, departure_longitude),
                               (forced_latitude, forced_longitude), unit=Unit.MILES)
        distancefa = haversine((forced_latitude, forced_longitude),
                               (arrival_latitude, arrival_longitude), unit=Unit.MILES)
        distance = sum([distancedf, distancefa])
        airlines_object.Distance = distance
        airlines_object.save()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'airlines.html', {'airlines_data': result})


def switch_off(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    user_id = request.user.id
    pilot_list = UserList.objects.filter(id=user_id).first()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    for item in result:
        item.ForcedPoint = 'Absent'
        item.AirFlight_status = 'Straight'
        item.Weather = 'Favorable'
        item.Description_weather = 'Sunny'
        departure = item.DeparturePoint
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departure)
        departure_latitude = location.latitude
        departure_longitude = location.longitude
        arrival = item.ArrivalPoint
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(arrival)
        arrival_latitude = location.latitude
        arrival_longitude = location.longitude
        distanceda = haversine((departure_latitude, departure_longitude),
                               (arrival_latitude, arrival_longitude), unit=Unit.MILES)
        item.Distance = distanceda
        item.save()
    return redirect('/airflight/')






