from django.shortcuts import render
from django.views.generic.list import ListView
#from django.views.generic import TemplateView
from apps.kardex.models import Kardex, Periodo, LineaPeriodo
from apps.transaccionInventario.models import *
from apps.producto.models import  Producto
from datetime import datetime
from django.db.models import Q



def inventario(request):
    return render(request, 'inventario/inventario.html')

#class ListaKardex(ListView):
#	model= Kardex
#	template_name='inventario/inventario.html'

def listKardex(request, periodoID):
	periodo= Periodo.objects.get(idPeriodo=periodoID)
	kardex= Kardex.objects.filter(idKardex= periodo.kardex.idKardex)	
	lineasPeriodo= LineaPeriodo.objects.filter(periodo=periodo)
	comprobacion=0
	for Comprobacion in lineasPeriodo:
		comprobacion= comprobacion+ Comprobacion.comprobacion
	contexto= {'kardex':kardex, 'lineaPeriodo':lineasPeriodo,'comprobacion':comprobacion}
	return render(request, 'inventario/inventario.html', contexto)

def listPeriodo(request, productoID):
	kardex= Kardex.objects.get(producto=productoID)
	periodo = Periodo.objects.filter(kardex=kardex).order_by('-fechaInicio')
	contexto= {'periodo':periodo, 'kardex':kardex}
	return render(request, 'inventario/listPeriodos.html',contexto)







#Agregar en transaccion
	#transInventario= TransaccionInventario(fecha =request.POST['fecha'], cantidadComprada =request.POST['cantidad'], 
	#costoUnitario =request.POST['costoUnitario'], factura =request.POST['factura'], 
	#tipo =request.POST['tipo'], producto =request.POST['producto'])

#metodo en caso de una transaccion de tipo compra
def compra(transaccionInventario):
	#Busqueda del producto para modificar su existencia
	Producto = Producto.objects.get(idProducto= transaccionInventario.producto)	
	#Busqueda del kardex
	Kardex = Kardex.objects.get(producto=transaccionInventario.producto)
	#Busqueda de su ultimo periodo
	Periodo = Periodo.objects.filter(kardex=Kardex).last()
	#General
	lpFecha = transaccionInventario.fecha
	lpFactura = transaccionInventario.factura
	lpTipo = transaccionInventario.tipo
	lpValorUnitario = transaccionInventario.valorUnitario
	lpPeriodo = Periodo
	#Entradas
	lpCantidadEntrada = transaccionInventario.cantidadTransaccion
	lpValorEntrada = lpValorUnitario * lpCantidadEntrada
	#Salidas
	lpValorSalida = 0
	lpCantidadSalida = 0
	#Existencias
	#Validaciones si no hay lineas de Periodo anteriores
	if LineaPeriodo.objects.filter(periodo=Periodo).exists()==True:
		lpAnterior = LineaPeriodo.objects.filter(periodo=Periodo).last()
		lpCantidadExistencia = lpAnterior.cantidadExistencia + lpCantidadEntrada
		lpValorExistencia = lpAnterior.valorExistencia + lpValorEntrada
	else :	
		lpCantidadExistencia= lpCantidadEntrada
		lpValorExistencia= lpValorEntrada	
	#Comprobacion
	lpCantidadSobrante = lpCantidadEntrada
	lpComprobacion = lpCantidadSobrante * lpValorUnitario
		#Guardando la nueva linea del periodo
	lineaperiodo = LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida, cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,comprobacion = lpComprobacion, compraAsociada=0,periodo= lpPeriodo)
	lineaperiodo.save()
	Producto.existencias= lineaperiodo.cantidadExistencia



#metodo en caso de transaccion de tipo Venta
def venta(transaccionInventario):
#Busqueda del producto para modificar su existencia
	Producto = Producto.objects.get(idProducto= transaccionInventario.producto)		
#Busqueda del kardex
	Kardex = Kardex.objects.get(producto=transaccionInventario.producto)
#Busqueda de su ultimo periodo
	Periodo = Periodo.objects.get(kardex=Kardex).last()
#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=Periodo).last()
#Primera compra cuya cantidad sobrante sea >0
	lcPrimera = LineaPeriodo.objects.filter(Q(periodo=Periodo, cantidadSobrant__gt=0, tipo='C')|Q(periodo=Periodo, cantidadSobrant__gt=0, tipo='I')).first()
#logica 
	#General
	lpFecha= transaccionInventario.fecha
	lpFactura= transaccionInventario.factura
	lpTipo= transaccionInventario.tipo
	lpValorUnitario= lcPrimera.valorUnitario
	lpPeriodo= Periodo
	#Entrada
	lpCantidadEntrada=0
	lpValorEntrada= 0
	#Comprobacion
	lpCantidadSobrante= 0
	lpComprobacion= 0
	#Campo exclusivo para Ventas
	lpCompraAsociada= lcPrimera.idLineaPeriodo		
#Si la cantidad de venta es menor a la primera compra con con existencia mayor que 0
	if transaccionInventario.cantidadTransaccion<lcPrimera.cantidadSobrante:		
		#Salidas	
		lpCantidadSalida=transaccionInventario.cantidadTransaccion
		lpValorSalida=lpValorUnitario * lpCantidadSalida
		#Existencias
		lpCantidadExistencia= lpAnterior.cantidadExistencia - lpCantidadSalida		
		lpValorExistencia=lpAnterior.valorExistencia - lpValorSalida		
		#Creacion de la nueva linea del periodo
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    		cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    		valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    		cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo)
		lineaperiodo.save()
		#Cambiando la comprobacion de la compra que redujo cantidad sobrante
		lcPrimera.cantidadSobrante= lcPrimera.cantidadSobrante- lpCantidadSalida
		lcPrimera.comprobacion= lcPrimera.cantidadSobrante* lcPrimera.valorUnitario
		lcPrimera.save()
		Producto.existencias= lineaperiodo.cantidadExistencia
	#Si la cantidad de venta es mayor a la primera compra con con existencia mayor que 0	
	if transaccionInventario.cantidadTransaccion>lcPrimera.cantidadSobrante:
		#Salida		
		lpCantidadSalida= lcPrimera.cantidadSobrante
		lpValorSalida=lpValorUnitario * lpCantidadSalida
		#Existencias
		lpCantidadExistencia= lpAnterior.cantidadExistencia - lpCantidadSalida	
		lpValorExistencia=lpAnterior.valorExistencia - lpValorSalida
		#Creacion de la nueva linea de periodo
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    		cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    		valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    		cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo)
		lineaperiodo.save()
		#Guardando comprobacion de la compra afectada
		lcPrimera.cantidadSobrante= 0
		lcPrimera.comprobacion= 0
		lcPrimera.save()
		Producto.existencias= lineaperiodo.cantidadExistencia
		#cantidad de productos que falta por vender	
		ventaFaltantante= transaccionInventario.cantidadTransaccion- lpCantidadSalida
		while ventaFaltantante>0:
			ventaFaltantante = ventaRepeticion(ventaFaltantante, Kardex, Periodo, lpFecha,lpFactura, lpTipo, Producto)

    	

#Metodo para crear multiples lineas de ventas si esta se hace de diferentes lineas de compra
def ventaRepeticion(ventafaltantante, Kardex, Periodo, Fecha, Factura, Tipo, producto):
	Producto=producto
	#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=lpPeriodo).last()
#Primera compra cuya cantidad sobrante sea >0
	lcPrimera = LineaPeriodo.objects.filter(Q(periodo=Periodo, cantidadSobrant__gt=0, tipo='C')|Q(periodo=Periodo, cantidadSobrant__gt=0, tipo='I')).first()
	#General
	lpFecha= Fecha
	lpFactura= Factura
	lpTipo=Tipo
	lpPeriodo= Periodo
	lpValorUnitario= lcPrimera.valorUnitario
	#Entradas
	lpCantidadEntrada=0
	lpValorEntrada= 0
	#Comprobacion
	lpCantidadSobrante= 0
	lpComprobacion= 0
	#Campo Exclusivo para Ventas
	lpCompraAsociada= lcPrimera.idLineaPeriodo
	#Salidas
	if ventafaltantante<lcPrimera.cantidadSobrante:		
		#Salidas	
		lpCantidadSalida=ventafaltantante
		lpValorSalida=lpValorUnitario * lpCantidadSalida
		#Existencias
		lpCantidadExistencia= lpAnterior.cantidadExistencia - lpCantidadSalida		
		lpValorExistencia=lpAnterior.valorExistencia - lpValorSalida		
		#Creacion de la nueva linea del periodo
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    		cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    		valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    		cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo)
		lineaperiodo.save()
		#Cambiando la comprobacion de la compra que redujo cantidad sobrante
		lcPrimera.cantidadSobrante= lcPrimera.cantidadSobrante- lpCantidadSalida
		lcPrimera.comprobacion= lcPrimera.cantidadSobrante* lcPrimera.valorUnitario
		lcPrimera.save()
		Producto.existencias= lineaperiodo.cantidadExistencia
		ventaFaltantanteNueva=0
	if transaccionInventario.cantidadTransaccion>lcPrimera.cantidadSobrante:
		#hacer comprobacion de ventasobrante>= cantidadSobrante
		lpCantidadSalida= lcPrimera.cantidadSobrante
		lpValorSalida=lpValorUnitario * lpCantidadSalida
		#Existencias
		lpCantidadExistencia= lpAnterior.cantidadExistencia - lpCantidadSalida	
		lpValorExistencia=lpAnterior.valorExistencia - lpValorSalida	
		#Guardar la nueva linea de periodo	
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
	    	cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    		valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    		cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo)
		lineaperiodo.save()
		#Cambiar comprobacion de la compra afectada
		lcPrimera.cantidadSobrante= lcPrimera.cantidadSobrante- lpCantidadSalida
		lcPrimera.comprobacion= lcPrimera.cantidadSobrante* lcPrimera.valorUnitario
		lcPrimera.save()
		Producto.existencias= lineaperiodo.cantidadExistencia
		ventaFaltantanteNueva = ventafaltantante- lpCantidadSalida  
	return ventaFaltantanteNueva

def devolucionCompra(transaccionInventario):
	#validacion factura, y que la devolucion sea menoro igual a la cantidad en la compra

#Busqueda del producto para modificar su existencia
	Producto = Producto.objects.get(idProducto= transaccionInventario.producto)
	#Busqueda del kardex
	Kardex = Kardex.objects.get(producto=transaccionInventario.producto)
	#Busqueda de su ultimo periodo
	Periodo = Periodo.objects.filter(kardex=Kardex).last()
	#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=Periodo).last()
	#Busqueda de la compra asociada con la devolucion
	lcDevolucion = LineaPeriodo.objects.get(Q(periodo=Periodo, tipo='C', factura= transaccionInventario.factura)|Q(periodo=Periodo, tipo='I', factura= transaccionInventario.factura))
	#General
	lpFecha = transaccionInventario.fecha
	lpFactura = transaccionInventario.factura
	lpTipo = transaccionInventario.tipo
	lpValorUnitario = lcDevolucion.valorUnitario
	lpPeriodo = Periodo
	#Entradas
	lpCantidadEntrada = -transaccionInventario.cantidadTransaccion
	lpValorEntrada = lpValorUnitario * lpCantidadEntrada
	#Salidas
	lpValorSalida = 0
	lpCantidadSalida = 0
	#Existencias
	lpCantidadExistencia = lpAnterior.cantidadExistencia + lpCantidadEntrada
	lpValorExistencia = lpAnterior.valorExistencia + lpValorEntrada
	#Comprobacion
	lpCantidadSobrante = 0
	lpComprobacion = 0
		#Guardando la nueva linea del periodo
	lineaperiodo = LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida, cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,comprobacion = lpComprobacion, compraAsociada=0,periodo= lpPeriodo)
	lineaperiodo.save()
	#Modificacion de la compra afectada
	lcDevolucion.cantidadSobrante= lcDevolucion.cantidadSobrante + lpCantidadEntrada
	lcDevolucion.comprobacion= lcDevolucion.cantidadSobrante* lcDevolucion.valorUnitario
	lcDevolucion.save()
	Producto.existencias= lineaperiodo.cantidadExistencia


def devolucionVenta(transaccionInventario):
	
	#validacion factura, y que la devolucion sea menoro igual a la cantidad en la compra

#Busqueda del producto para modificar su existencia
	Producto = Producto.objects.get(idProducto= transaccionInventario.producto)
	#Busqueda del kardex
	Kardex = Kardex.objects.get(producto=transaccionInventario.producto)
	#Busqueda de su ultimo periodo
	Periodo = Periodo.objects.filter(kardex=Kardex).last()
	#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=Periodo).last()
	#Busqueda de las ventas asociadas con la devolucion
	ventas= LineaPeriodo.objects.filter(periodo=Periodo, tipo='V', factura= transaccionInventario.factura)
	for venta in ventas:
		compraAsociada = LineaPeriodo.objects.get(idLineaPeriodo= venta.ventaAsociada)
		#General
		lpFecha = transaccionInventario.fecha
		lpFactura = transaccionInventario.factura
		lpTipo = transaccionInventario.tipo
		lpValorUnitario = compraAsociada.valorUnitario
		lpPeriodo = Periodo
		#Entradas
		lpCantidadEntrada = 0
		lpValorEntrada = 0
		#Salidas
		lpValorSalida = -transaccionInventario.cantidadTransaccion
		lpCantidadSalida = lpValorUnitario * lpCantidadEntrada
		#Existencias
		lpCantidadExistencia = lpAnterior.cantidadExistencia - lpCantidadSalida
		lpValorExistencia = lpAnterior.valorExistencia - lpValorSalida
		#Comprobacion
		lpCantidadSobrante = 0
		lpComprobacion = 0
		#Creacion de la nueva linea
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    	cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    	valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    	cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    	comprobacion = lpComprobacion, compraAsociada=0, periodo= lpPeriodo)
		lineaperiodo.save()
		#Actualizando comprobacion de compra Asociada
		compraAsociada.cantidadSobrante= compraAsociada.cantidadSobrante - lpCantidadSalida
		compraAsociada.comprobacion= compraAsociada.cantidadSobrante* compraAsociada.valorUnitario
		compraAsociada.save()
		Producto.existencias= lineaperiodo.cantidadExistencia



def cierreContableKardex(parametro):
	productos = Producto.objects.all()
	for producto in productos:
		Kardex = Kardex.objects.get(producto=producto)
		#filtrando el ultimo periodo de cada Kardex y asignando su saldo y existencia final
		Periodo = Periodo.objects.filter(kardex=Kardex).last()
		#La fecha deberia ser cuando den click en cierre contable, pero por facilidad sera cuando decidamos
		fecha = parametro.fecha
		Periodo.fechaFinal = fecha
		lpUltima = LineaPeriodo.objects.filter(periodo=Periodo).last()
		Periodo.existenciaFinal= lpUltima.cantidadExistencia
		Periodo.saldoFinal= lpUltima.valorExistencia
		Periodo.save()
		#Creando el nuevo periodo para cada Kardex
		diaSiguiente= fecha + datetime.timedelta(days=1)
		periodoNuevo= Periodo(fechaInicio = diaSiguiente ,existenciaFinal=0,saldoFinal =0,kardex= Kardex)
		periodoNuevo.save()
		#productos sobrantes de periodo anterior pasan a inventario inicial del nuevo Periodo
		existenciasSobrantes= LineaPeriodo.objects.filter(tipo='C', periodo=Periodo, cantidadSobrante__gt=0)
		for existencia in existenciasSobrantes:
			invInicial= existencia
			invInicial.periodo= periodoNuevo
			invInicial.fecha= diaSiguiente
			#convirtiendo a inventario inicial productos sobrantes
			invInicial.tipo='I'
			#valores de entrada
			invInicial.cantidadEntrada= invInicial.cantidadSobrante
			invInicial.valorEntrada = invInicial.cantidadEntrada* invInicial.valorUnitario
			#Validaciones si no hay lineas de Periodo anteriores
			if LineaPeriodo.objects.filter(periodo=compra.periodo).exists()==True:
				lpAnterior = LineaPeriodo.objects.filter(periodo=Periodo).last()
				invInicial.cantidadExistencia = lpAnterior.cantidadExistencia + invInicial.cantidadEntrada
				invInicial.valorExistencia = lpAnterior.valorExistencia + invInicial.valorEntrada
			else :	
				invInicial.cantidadExistencia= invInicial.cantidadEntrada
				invInicial.valorExistencia= invInicial.valorEntrada
			invInicial.save()
			



	