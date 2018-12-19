from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from utils import cancel_info
from notify.management.commands.collect import date_normalize


@login_required
def own_info(request):
    user = request.user
    grade = user.grade_set.all()[0].grade
    major = user.major_set.all()[0].initial
    if grade <= 2:
        lgc = user.lowgradeclass_set.all()[0].low_grade_class
    else:
        lgc = None

    cancels = cancel_info.just_for_you(grade, major, lgc)
    [date_normalize(cancel) for cancel in cancels]

    context = {'cancels': cancels}

    return render(request, 'info.html', context=context)
