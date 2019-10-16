from django.urls import path
from django.conf.urls import url
from apps.kardex.views import inventario

urlpatterns = [
    path('', inventario, name="inventario"),
]