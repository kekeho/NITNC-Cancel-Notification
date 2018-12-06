from django.shortcuts import render


def index(request):
    context = {}
    context['user'] = request.user  # ログインユーザー

    return render(request, "index.html", context=context)
