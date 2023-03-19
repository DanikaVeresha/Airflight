import datetime
import random
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from django.shortcuts import render, redirect
from django.http import HttpResponse
from airflight.models import AirLines, AirCompany, DeparturePoint, ArrivalPoint, UserList, ForcedPoint


def add_AirLines(request):
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
        dlatitude = location.latitude
        dlongitude = location.longitude
        departurepoint_object = DeparturePoint(DeparturePoint_name=departurepoint,
                                               DeparturePoint_latitude=dlatitude,
                                               DeparturePoint_longitude=dlongitude,
                                               AirFlight_id=pilot_list.AirFlight_id)
        departurepoint_object.save()
        arrivalpoint = request.POST.get('adress_airoporte')
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departurepoint)
        alatitude = location.latitude
        alongitude = location.longitude
        arrivalpoint_object = ArrivalPoint(ArrivalPoint_name=arrivalpoint,
                                           ArrivalPoint_latitude=alatitude,
                                           ArrivalPoint_longitude=alongitude,
                                           AirFlight_id=pilot_list.AirFlight_id)
        arrivalpoint_object.save()
        airlines_object = AirLines(AirCommpany=aircommpany_object.AirCommpany,
                                   DeparturePoint=departurepoint_object.DeparturePoint_name,
                                   ArrivalPoint=arrivalpoint_object.ArrivalPoint_name,
                                   AirFlight_id=pilot_list.AirFlight_id,
                                   AirFlight_departure_date=datetime.datetime.now(),
                                   Distance=haversine((departurepoint_object.DeparturePoint_latitude, departurepoint_object.DeparturePoint_longitude),
                                                      (arrivalpoint_object.ArrivalPoint_latitude, arrivalpoint_object.ArrivalPoint_longitude), unit=Unit.MILES))
        airlines_object.save()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'airlines.html', {'airlines_data': result})


def changed_AirLines_weather(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    if request.method == 'POST':
        flight_obj = AirLines.objects.get(id=item_id)
        flight_obj.AirFlight_status = 'Changed'
        flight_obj.Weather = 'Not favorable'
        flight_obj.Description_weather = 'A threat has been detected on your course (weather conditions)'
        startPoint = DeparturePoint.objects.get(DeparturePoint_latitude=flight_obj.DeparturePoint.DeparturePoint_latitude,
                                                DeparturePoint_longitude=flight_obj.DeparturePoint.DeparturePoint_longitude)
        trtPoint = ForcedPoint.objects.get(ForcedPoint_latitude=flight_obj.ForcedPoint.ForcedPoint_latitude,
                                           ForcedPoint_longitude=flight_obj.ForcedPoint.ForcedPoint_longitude)
        distance_obj = haversine((startPoint.DeparturePoint_latitude, startPoint.DeparturePoint_longitude),
                                 (trtPoint.ForcedPoint_latitude, trtPoint.ForcedPoint_longitude), unit=Unit.MILES)
        finishPoint = ArrivalPoint.objects.get(ArrivalPoint_latitude=flight_obj.ArrivalPoint.ArrivalPoint_latitude,
                                               ArrivalPoint_longitude=flight_obj.ArrivalPoint.ArrivalPoint_longitude)
        distance_object = haversine((trtPoint.ForcedPoint_latitude, trtPoint.ForcedPoint_longitude),
                                    (finishPoint.ArrivalPoint_latitude, finishPoint.ArrivalPoint_longitude), unit=Unit.MILES)
        flight_obj.Distance = distance_obj + distance_object
        flight_obj.save()
    return redirect('/airflifht/airlines')


def add_ForcedPoint(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    user_id = request.user.id
    pilot_list = UserList.objects.filter(id=user_id).first()
    if request.method == 'POST':
        forcedpoint = request.POST.get('adress_airoport')
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(forcedpoint)
        latitude = location.latitude
        longitude = location.longitude
        forcedpoint_object = ForcedPoint(ForcedPoint_name=forcedpoint,
                                         ForcedPoint_latitude=latitude,
                                         ForcedPoint_longitude=longitude,
                                         AirFlight_id=pilot_list.AirFlight_id)
        forcedpoint_object.save()
    result = ForcedPoint.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'add_forcedpoint.html', {'forcedpoint_data': result})



