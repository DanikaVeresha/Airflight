from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_launch, name='flight_launch'),
]

