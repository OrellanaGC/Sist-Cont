from django.urls import path
from django.conf.urls import url
from apps.usuario.views import resumenUsuarios, crearUsuario, actualizarMiUsuario

urlpatterns = [
    path('', resumenUsuarios, name="resumenUsuarios"),
    path('crear', crearUsuario, name="crearUsuario"),
    path('actualizar_informacion', actualizarMiUsuario, name="actualizarMiUsuario"),
]
