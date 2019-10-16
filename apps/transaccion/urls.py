from django.urls import path
from django.conf.urls import url
from apps.transaccion.views import nuevaPartida, agregarTransaccion, eliminarTransaccion, resumenPartida

urlpatterns = [
    path('', resumenPartida, name="resumenPartida"),
    path('nueva', nuevaPartida, name="nuevaPartida"),
    path('agregar', agregarTransaccion, name='agregarTransaccion'),
    path('eliminar/<int:idTransaccion>', eliminarTransaccion, name='transaccionElminar')
]