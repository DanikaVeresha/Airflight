from django.urls import path
from . import views

urlpatterns = [
    path('/airlines', views.add_AirLines, name='add_AirLines'),
    path('/forcedpoint', views.add_ForcedPoint, name='add_ForcedPoint'),
]
