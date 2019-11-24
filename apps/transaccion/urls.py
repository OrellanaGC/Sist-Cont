from django.urls import path
from django.conf.urls import url
from apps.transaccion.views import nuevaPartida, agregarTransaccion, eliminarTransaccion, resumenPartida, cargarXCP, cancelarPartidaDoble, cargarXCPFe

urlpatterns = [
    path('', resumenPartida, name="resumenPartida"),
    path('<int:cuentaPadre>', cargarXCP, name="cargarXCP"),
    path('<int:cuentaPadre>/<int:anio>/<int:mes>', cargarXCPFe, name="cargarXCPFe"),
    path('nueva', nuevaPartida, name="nuevaPartida"),
    path('agregar', agregarTransaccion, name='agregarTransaccion'),
    path('eliminar', eliminarTransaccion, name='transaccionElminar'),
    path('cancelar/<str:idsTransacc>',cancelarPartidaDoble, name="cancelarPar")
]