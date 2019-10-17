from django.urls import path
from django.conf.urls import url
from apps.cuenta.views import resumenCuenta, nuevaCuenta

urlpatterns = [
    path('', resumenCuenta, name="resumenCuenta"),
    path('crear', nuevaCuenta, name="nuevaCuenta"),
]
