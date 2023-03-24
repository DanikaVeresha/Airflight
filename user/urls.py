from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_pilot, name='login_pilot'),
    path('register', views.register_pilot, name='register_pilot'),
    path('logout', views.logout_pilot, name='logout_pilot'),
]




