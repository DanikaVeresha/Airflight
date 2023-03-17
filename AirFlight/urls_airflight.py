from django.urls import path
from . import views

urlpatterns = [
    path('/add_AirLines', views.add_AirLines, name='add_AirLines'),
    path('/add_ForcedPoint', views.add_ForcedPoint, name='add_ForcedPoint'),
]