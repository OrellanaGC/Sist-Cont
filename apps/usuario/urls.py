from django.urls import path
from django.conf.urls import url
from apps.usuario.views import resumenUsuarios, crearUsuario
from apps.usuario.views import actualizarMiUsuario, eliminarUsuario
from apps.usuario.views import actualizarUsuario, actualizarMiUsuarioResumen

urlpatterns = [
    path('', resumenUsuarios, name="resumenUsuarios"),
    path('crear', crearUsuario, name="crearUsuario"),
    path('miUsuario', actualizarMiUsuarioResumen, name="miUsuario"),
    path('editarMiUsuario', actualizarMiUsuario, name="editarMiUsuario"),
    path('editar/<int:idUsuario>', actualizarUsuario, name="actualizarUsuario"),
    path('eliminar/<int:idUsuario>', eliminarUsuario, name="eliminarUsuario"),
]
