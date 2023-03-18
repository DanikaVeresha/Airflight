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
    pilot_list = UserList.objects.filter(id=12).first()
    if request.method == 'POST':
        aircommpany = request.POST.get('aircommpany')
        aircommpany_object = AirCompany(AirCommpany=aircommpany)
        aircommpany_object.save()
        departurepoint = request.POST.get('adress_airoport')
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departurepoint)
        dlatitude = location.latitude
        dlongitude = location.longitude
        departurepoint_object = DeparturePoint(DeparturePoint_name=departurepoint,
                                               DeparturePoint_latitude=dlatitude,
                                               DeparturePoint_longitude=dlongitude)
        departurepoint_object.save()
        arrivalpoint = request.POST.get('adress_airoporte')
        geolocator = Nominatim(user_agent="airflight")
        location = geolocator.geocode(departurepoint)
        alatitude = location.latitude
        alongitude = location.longitude
        arrivalpoint_object = ArrivalPoint(ArrivalPoint_name=arrivalpoint,
                                           ArrivalPoint_latitude=alatitude,
                                           ArrivalPoint_longitude=alongitude)
        arrivalpoint_object.save()
        airfight_price_object = request.POST.get('airfight_price')
        distance_object = haversine((dlatitude, dlongitude), (alatitude, alongitude), unit=Unit.MILES)
        airlines_object = AirLines(AirCompany=aircommpany_object,
                                   DeparturePoint=departurepoint_object,
                                   ArrivalPoint=arrivalpoint_object,
                                   AirFight_price=airfight_price_object,
                                   Distance=distance_object)
        airlines_object.AirFlight_departure_date = datetime.datetime.now()
        airlines_object.save()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'airlines.html', {'airlines_data': result})


def changed_AirLines_weather(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    if request.method == 'POST':
        forcedpoint_bjc = random.choice(ForcedPoint.objects.all())
        ForcedPoint_bject = AirLines(ForcedPoint=forcedpoint_bjc)
        ForcedPoint_bject.save()
        AirFlight_status_object = AirLines(AirFlight_status='Changed')
        AirFlight_status_object.AirFlight_status.save()
        Weather_object = AirLines(Weather='Not favorable')
        Weather_object.Weather.save()
        Description_weather_object = AirLines(Description_weather='A threat has been detected on your course (weather conditions)')
        Description_weather_object.save()
        startPoint = DeparturePoint.objects.get(DeparturePoint_latitude=DeparturePoint.DeparturePoint_latitude,
                                                DeparturePoint_longitude=DeparturePoint.DeparturePoint_longitude)
        trtPoint = ForcedPoint.objects.get(ForcedPoint_latitude=ForcedPoint.ForcedPoint_latitude,
                                           ForcedPoint_longitude=ForcedPoint.ForcedPoint_longitude)
        distance_obj = haversine((startPoint.DeparturePoint_latitude, startPoint.DeparturePoint_longitude),
                                 (trtPoint.ForcedPoint_latitude, trtPoint.ForcedPoint_longitude), unit=Unit.MILES)
        finishPoint = ArrivalPoint.objects.get(ArrivalPoint_latitude=ArrivalPoint.ArrivalPoint_latitude,
                                               ArrivalPoint_longitude=ArrivalPoint.ArrivalPoint_longitude)
        distance_object = haversine((trtPoint.ForcedPoint_latitude, trtPoint.ForcedPoint_longitude),
                                    (finishPoint.ArrivalPoint_latitude, finishPoint.ArrivalPoint_longitude), unit=Unit.MILES)
        total_distance = sum(distance_obj, distance_object)
        AirLines_object = AirLines(ForcedPoint=forcedpoint_bjc,
                                   AirFlight_status=AirFlight_status_object,
                                   Weather=Weather_object,
                                   Description_weather=Description_weather_object,
                                   Distance=total_distance)
        AirLines_object.save()
    return redirect('/airflifht')


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
                                         ForcedPoint_longitude=longitude)
        forcedpoint_object.save()
    result = ForcedPoint.objects.filter(ForcedPoint_id=pilot_list.ForcedPoint_id)
    return render(request, 'add_forcedpoint.html', {'forcedpoint_data': result})


