from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Grade, Major, LowGradeClass


def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        grade = int(request.POST['grade'])
        major = request.POST['major']
        low_grade_class = int(request.POST['class'])

        already_user = User.objects.filter(email=email)
        if len(already_user) == 0:
            user = User.objects.create_user(username=username, email=email,
                                            password=password)
            Grade.objects.get(grade=grade).user.add(user)
            Major.objects.get(initial=major).user.add(user)
            if low_grade_class:
                LowGradeClass.objects.get(low_grade_class=low_grade_class
                                          ).user.add(user)
            
            login(request, user)
            return redirect('/')
        else:
            context = {'message': 'サインアップ失敗。すでに登録されているユーザーの可能性があります'}
            return render(request, 'registration/signup.html', context)
    else:
        # GET
        return render(request, 'registration/signup.html')


def login_func(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request=request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'login_error': 'ログインに失敗しました'}
            return render(request, 'registration/login.html', context)
    else:
        # GET
        context = {}
        if request.user.id:
            context['message'] = 'すでにログイン済みです'

        return render(request, 'registration/login.html', context)


def logout_func(request):
    logout(request)
    return redirect('/')
