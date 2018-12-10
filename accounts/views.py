from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def signup(request):
    if request.GET:
        return render(request, 'signup.html')

    elif request.POST:
        email = request.POST['email']


def login_func():
    pass


def logout():
    pass
