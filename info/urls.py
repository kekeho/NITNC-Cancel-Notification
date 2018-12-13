from django.urls import path
from . import views

urlpatterns = [
    path('', views.own_info, name='info_index')
]
