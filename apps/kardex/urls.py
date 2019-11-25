from django.urls import path
from django.conf.urls import url
from django.views.generic.list import ListView
#from apps.kardex.views import inventario
from apps.kardex.views import  listKardex, listPeriodo

urlpatterns = [
    #path('', inventario, name="inventario"),
    #path('', ListaKardex.as_view() , name='inventario'),
    path('periodos/<int:periodoID>', listKardex,name='inventario'),
    path('<int:productoID>', listPeriodo,name='Periodos')

]