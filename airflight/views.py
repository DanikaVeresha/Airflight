import datetime
import random
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from django.shortcuts import render, redirect
from airflight.models import AirLines, AirCompany, DeparturePoint, ArrivalPoint, UserList, ForcedPoint


def normal_mode(request):
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
                                   AirFlight_departure_date=datetime.datetime.now())
        airlines_object.Distance = haversine((departurepoint_object.DeparturePoint_latitude, departurepoint_object.DeparturePoint_longitude),
                                                        (arrivalpoint_object.ArrivalPoint_latitude, arrivalpoint_object.ArrivalPoint_longitude), unit=Unit.MILES)
        airlines_object.save()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'airlines.html', {'airlines_data': result})


def potential_threat_mode(request):
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
        distance = haversine((departurepoint_object.DeparturePoint_latitude, departurepoint_object.DeparturePoint_longitude),
                             (arrivalpoint_object.ArrivalPoint_latitude, arrivalpoint_object.ArrivalPoint_longitude), unit=Unit.MILES)
        trtPoint = ForcedPoint.objects.filter(AirFlight_id=pilot_list.AirFlight_id).all()
        for item in trtPoint:
            trt_distance = haversine((departurepoint_object.DeparturePoint_latitude, departurepoint_object.DeparturePoint_longitude),
                                     (item.ForcedPoint_latitude, item.ForcedPoint_longitude), unit=Unit.MILES)
            if trt_distance < distance:
                trt_item = ForcedPoint.objects.filter(ForcedPoint_name=item.ForcedPoint_name).first()
                airlines_object = AirLines(AirCommpany=aircommpany_object.AirCommpany,
                                           DeparturePoint=departurepoint_object.DeparturePoint_name,
                                           ArrivalPoint=arrivalpoint_object.ArrivalPoint_name,
                                           AirFlight_id=pilot_list.AirFlight_id,
                                           AirFlight_departure_date=datetime.datetime.now(),
                                           ForcedPoint=trt_item.ForcedPoint_name,
                                           AirFlight_status='Changed',
                                           Weather='Not favorable',
                                           Description_weather='Thunderstorm or no-fly zone')
                airlines_object.Distance = trt_distance + haversine((item.ForcedPoint_latitude, item.ForcedPoint_longitude),
                                                                    (arrivalpoint_object.ArrivalPoint_latitude, arrivalpoint_object.ArrivalPoint_longitude), unit=Unit.MILES)
                airlines_object.save()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'airlines_threat.html', {'airlines_threat_data': result})


def add_forcedPoint(request):
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



