from django.urls import path
from django.conf.urls import url
from apps.empresa.views import resumenEmpresa

urlpatterns = [
    path('', resumenEmpresa, name="resumenEmpresa"),
]
