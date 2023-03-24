from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_launch, name='flight_launch'),
    path('switch_off', views.switch_off, name='switch_off'),
]

