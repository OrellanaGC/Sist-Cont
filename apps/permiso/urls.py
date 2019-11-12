from django.urls import path
from django.conf.urls import url
from apps.permiso.views import resumenPermiso, eliminarPermiso

urlpatterns = [
    path('', resumenPermiso, name="resumenPermiso"),
    path('eliminar/<int:idCuenta>', eliminarPermiso, name="eliminarPermiso"),
]
