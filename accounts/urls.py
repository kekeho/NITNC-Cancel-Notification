from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_func, name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('profile/', views.profile, name='profile'),
]
