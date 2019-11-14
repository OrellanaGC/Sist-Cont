from django.urls import path
from django.conf.urls import url
from apps.permiso.views import resumenPermiso, eliminarPermiso, editarPermiso

urlpatterns = [
    path('', resumenPermiso, name="resumenPermiso"),
    path('<int:idPermiso>', editarPermiso, name="editarPermiso"),
    path('eliminar/<int:idPermiso>', eliminarPermiso, name="eliminarPermiso"),
]
