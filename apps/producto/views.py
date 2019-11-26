from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from apps.producto.models import Producto
from apps.producto.forms import ProductoForm, transInvForm
from apps.kardex.models import Kardex, Periodo
from apps.kardex.views import *
from django.views.generic import ListView, CreateView
from datetime import datetime

def CreateProducto(request):	
	if request.method == 'GET':
		form = ProductoForm()
	else:
		form = ProductoForm(request.POST)
		if form.is_valid():			
			form.save()
			producto= form.save()
			kardex = Kardex(producto = producto)
			kardex.save()
			fecha = datetime.now()
			periodo= Periodo(fechaInicio = fecha ,existenciaFinal=0,saldoFinal =0,kardex= kardex)
			periodo.save()
		return redirect('verProducto')
	return render(request, 'productos/registrarProducto.html', {'form':form})

#Create para transaccion Inventario
def CreateTransaccion(request):	
	if request.method == 'GET':
		form = transInvForm()
	else:
		form = transInvForm(request.POST)
		if form.is_valid():			
			form.save()	
		transaccionInv= form.save()
		if transaccionInv.tipo == 'C':
			compra(transaccionInv)
		if transaccionInv.tipo == 'V':
			venta(transaccionInv)
		if transaccionInv.tipo == 'DC':
			devolucionCompra(transaccionInv)
		if transaccionInv.tipo == 'DV':
			devolucionVenta(transaccionInv)		
		return redirect('registrarTransaccion')
	return render(request, 'productos/registrarTransaccion.html', {'form':form})





def ListProducto(request):
	if request.method =='GET':
		producto= Producto.objects.all().order_by('-idProducto')	
		contexto={'productos':producto}
	else:
		fecha = request.POST['fechaK']
		cierreContableKardex(fecha)
		return redirect('verProducto')
	return render(request, 'productos/verProducto.html', contexto)
	

def UpdateProducto(request, productoID):
	producto = Producto.objects.get(idProducto = productoID)
	if request.method == 'GET':
		form = ProductoForm(instance=producto)
	else:
		form = ProductoForm(request.POST, instance=producto)
		if form.is_valid():
			form.save()			
		return redirect('verProducto')
	return render(request, 'productos/registrarProducto.html', {'form':form})