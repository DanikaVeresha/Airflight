from django.db import models


class Pilot(models.Model):
    Pilot_name = models.CharField(max_length=100)


class ExceptionFlight(models.Model):
    Exception_name = models.CharField(max_length=100)
    Exception_description = models.CharField(max_length=100)


# Create your models here.
class AirFlight(models.Model):
    Flight_id = models.UUIDField()
    Pilot = models.ForeignKey(Pilot.Pilot_name, on_delete=models.CASCADE)
    Exception = models.ForeignKey(ExceptionFlight.Exception_name, on_delete=models.CASCADE)
    Status_flight = models.CharField(default='straight', max_length=20)
    Flight_status_by_passengers = models.CharField(default='empty', max_length=20)
    Flight_type = models.CharField(default='passenger', max_length=20)
    Flight_price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    Flight_date = models.DateField(null=True)


class StartingPoint(models.Model):
    StartingPoint_name = models.CharField(max_length=100)
    Airport_latitude_coordinate = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    Airport_longitude_coordinate = models.DecimalField(decimal_places=2, max_digits=10, null=True)


class PointOfArrival(models.Model):
    PointOfArrival_name = models.CharField(max_length=100)
    Airport_latitude_coordinate = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    Airport_longitude_coordinate = models.DecimalField(decimal_places=2, max_digits=10, null=True)


class ExceptionPoint(models.Model):
    ExceptionPoint_name = models.CharField(max_length=100)
    Airport_latitude_coordinate = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    Airport_longitude_coordinate = models.DecimalField(decimal_places=2, max_digits=10, null=True)


class Flight(models.Model):
    Flight_id = models.UUIDField()
    StartingPoint = models.ForeignKey(StartingPoint.StartingPoint_name, on_delete=models.CASCADE)
    PointOfArrival = models.ForeignKey(PointOfArrival.PointOfArrival_name, on_delete=models.CASCADE)
    ExceptionPoint = models.ForeignKey(ExceptionPoint.ExceptionPoint_name, on_delete=models.CASCADE)


