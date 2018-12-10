from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User


def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        already_user = User.objects.filter(email=email)
        if len(already_user) == 0:
            user = User.objects.create_user(username=username, email=email,
                                            password=password)
            login(request, user)
            return redirect('/')
        else:
            context = {'message': 'サインアップ失敗。すでに登録されているユーザーの可能性があります'}
            return render(request, 'registration/signup.html', context)
    else:
        return render(request, 'registration/signup.html')


def login_func(request):
    pass


def logout():
    pass
