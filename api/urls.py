from django.urls import path

from api.views import login, register, test

urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('test/', test),
]