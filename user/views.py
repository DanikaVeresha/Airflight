from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from AirFlight.models import AirCompany, UserList


def login_pilot(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/add_AirLines')
        else:
            return redirect('/user/register')
    else:
        return render(request, 'login.html')


def register_pilot(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username, password)
        user.save()
        pilot_list = UserList(id=user.id, AirFlight_id=uuid.uuid4())
        pilot_list.save()
        pilot = AirCompany(id=user.id, AirFlight_id=uuid.uuid4())
        pilot.save()
        return redirect('/user/login')
    return render(request, 'register.html')


def logout_pilot(request):
    logout(request)
    return redirect('/user/login')
