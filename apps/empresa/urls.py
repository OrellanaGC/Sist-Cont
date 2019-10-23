from django.urls import path
from django.conf.urls import url
from apps.empresa.views import resumenEmpresa, guardarDatos

urlpatterns = [
    path('', resumenEmpresa, name="resumenEmpresa"),
    path('guardar', guardarDatos, name="guardarDatos")
]
