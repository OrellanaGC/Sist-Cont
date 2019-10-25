from django.urls import path
from django.conf.urls import url
#from apps.kardex.views import inventario
from apps.kardex.views import ListaKardex

urlpatterns = [
    #path('', inventario, name="inventario"),
    path('', ListaKardex.as_View() , name='inventario'),
]