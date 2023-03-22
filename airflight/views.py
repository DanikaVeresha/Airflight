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
        forcedpoint = ((departure_latitude + 0.05, departure_longitude - 0.05))
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
        distancedf = haversine((departurepoint_object.DeparturePoint_latitude,
                                departurepoint_object.DeparturePoint_longitude),
                               (forcedpoint_object.ForcedPoint_latitude,
                                forcedpoint_object.ForcedPoint_longitude), unit=Unit.METERS)
        distansefa = haversine((forcedpoint_object.ForcedPoint_latitude,
                                forcedpoint_object.ForcedPoint_longitude),
                               (arrivalpoint_object.ArrivalPoint_latitude,
                                arrivalpoint_object.ArrivalPoint_longitude), unit=Unit.METERS)
        distance = sum([distancedf, distansefa])
        airlines_object.Distance = distance
        airlines_object.save()
    result = AirLines.objects.filter(AirFlight_id=pilot_list.AirFlight_id)
    return render(request, 'airlines.html', {'airlines_data': result})




