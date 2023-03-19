from django.urls import path
from . import views

urlpatterns = [
    path('/normal_mode', views.normal_mode, name='normal_mode'),
    path('/potential_threat_mode', views.potential_threat_mode, name='potential_threat_mode'),
    path('/add_forcedPoint', views.add_forcedPoint, name='add_forcedPoint'),
]
