from django.urls import path
from django.conf.urls import url
from apps.permiso.views import resumenPermiso

urlpatterns = [
    path('', resumenPermiso, name="resumenPermiso"),
]
