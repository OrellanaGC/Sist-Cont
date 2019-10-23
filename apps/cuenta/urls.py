from django.urls import path
from django.conf.urls import url
from apps.cuenta.views import resumenCuenta, nuevaCuenta, modificarCuenta, eliminarCuenta

urlpatterns = [
    path('', resumenCuenta, name="resumenCuenta"),
    path('crear', nuevaCuenta, name="nuevaCuenta"),
    path('editar/<int:idCuenta>', modificarCuenta, name="modificarCuenta"),
    path('eliminar/<int:idCuenta>', eliminarCuenta, name="eliminarCuenta")
]
