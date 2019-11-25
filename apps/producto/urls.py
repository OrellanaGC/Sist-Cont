from django.urls import path
from django.conf.urls import url
from apps.producto.views import CreateProducto, ListProducto, UpdateProducto, CreateTransaccion 

urlpatterns = [
	path('', ListProducto, name="verProducto"),
	path('agregar', CreateProducto, name="registrarProducto"),	
	path('modificar/<int:productoID>', UpdateProducto, name="updateProducto"),
	path('transaccion/agregar', CreateTransaccion, name="registrarTransaccion"),	

    
]

