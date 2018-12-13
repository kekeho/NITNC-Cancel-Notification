from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def own_info(request):
    user = request.user
    grade = user.grade_set.all()[0].grade
    major = user.major_set.all()[0].initial
    if grade <= 2:
        lgc = user.low_grade_class_set.all()[0].low_grade_class
    else:
        lgc = None

    return HttpResponse(f"{grade} {major} {lgc}")
