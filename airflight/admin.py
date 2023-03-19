from django.contrib import admin
from .models import AirLines, ForcedPoint, UserList, DeparturePoint, ArrivalPoint, AirCompany

# Register your models here.
admin.site.register(AirCompany)
admin.site.register(DeparturePoint)
admin.site.register(ArrivalPoint)
admin.site.register(ForcedPoint)
admin.site.register(AirLines)
admin.site.register(UserList)

