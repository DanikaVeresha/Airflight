from django.db import models


class AirCompany(models.Model):
    AirFlight_id = models.UUIDField()
    AirCommpany = models.CharField(max_length=100)


class DeparturePoint(models.Model):
    AirFlight_id = models.UUIDField()
    DeparturePoint_name = models.CharField(max_length=100)
    DeparturePoint_latitude = models.DecimalField(decimal_places=2, max_digits=10)
    DeparturePoint_longitude = models.DecimalField(decimal_places=2, max_digits=10)


class ArrivalPoint(models.Model):
    AirFlight_id = models.UUIDField()
    ArrivalPoint_name = models.CharField(max_length=100)
    ArrivalPoint_latitude = models.DecimalField(decimal_places=2, max_digits=10)
    ArrivalPoint_longitude = models.DecimalField(decimal_places=2, max_digits=10)


class ForcedPoint(models.Model):
    AirFlight_id = models.UUIDField()
    ForcedPoint_name = models.CharField(max_length=200)
    ForcedPoint_latitude = models.DecimalField(decimal_places=2, max_digits=10)
    ForcedPoint_longitude = models.DecimalField(decimal_places=2, max_digits=10)


class AirLines(models.Model):
    AirFlight_id = models.UUIDField()
    AirCommpany = models.CharField(max_length=100)
    DeparturePoint = models.CharField(max_length=100)
    ArrivalPoint = models.CharField(max_length=100)
    ForcedPoint = models.CharField(max_length=100, null=True)
    AirFlight_departure_date = models.DateField(null=True)
    AirFlight_status = models.CharField(default='Straight', max_length=100)
    AirFlight_type = models.CharField(default='Passenger', max_length=100)
    Weather = models.CharField(default='Favorable', max_length=100)
    Description_weather = models.CharField(default='Sunny', max_length=100)
    Distance = models.FloatField()


class UserList(models.Model):
    user_id = models.IntegerField
    AirFlight_id = models.UUIDField()





