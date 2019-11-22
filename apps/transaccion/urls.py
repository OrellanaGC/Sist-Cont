from django.urls import path
from django.conf.urls import url
from apps.transaccion.views import nuevaPartida, agregarTransaccion, eliminarTransaccion, resumenPartida, cargarXCP, cancelarPartidaDoble

urlpatterns = [
    path('', resumenPartida, name="resumenPartida"),
    path('<int:cuentaPadre>', cargarXCP, name="cargarXCP"),
    path('nueva', nuevaPartida, name="nuevaPartida"),
    path('agregar', agregarTransaccion, name='agregarTransaccion'),
    path('eliminar', eliminarTransaccion, name='transaccionElminar'),
    path('cancelar/<str:idsTransacc>',cancelarPartidaDoble, name="cancelarPar")
]