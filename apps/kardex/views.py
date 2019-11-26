from django.shortcuts import render
from django.views.generic.list import ListView
#from django.views.generic import TemplateView
from apps.kardex.models import Kardex, Periodo, LineaPeriodo
from apps.transaccionInventario.models import *
from apps.producto.models import  Producto
import datetime
from django.db.models import Q



def inventario(request):
    return render(request, 'inventario/inventario.html')

#class ListaKardex(ListView):
#	model= Kardex
#	template_name='inventario/inventario.html'

def listKardex(request, periodoID):
	periodo= Periodo.objects.get(idPeriodo=periodoID)
	kardex= Kardex.objects.get(idKardex= periodo.kardex.idKardex)	
	lineasPeriodo= LineaPeriodo.objects.filter(periodo=periodo).order_by('idLineaPeriodo')
	comprobacion=0
	for Comprobacion in lineasPeriodo:
		comprobacion= comprobacion+ Comprobacion.comprobacion
	contexto= {'kardex':kardex, 'lineaPeriodo':lineasPeriodo,'comprobacion':comprobacion}
	return render(request, 'inventario/inventario.html', contexto)

def listPeriodo(request, productoID):
	kardex= Kardex.objects.get(producto=productoID)
	periodo = Periodo.objects.filter(kardex=kardex).order_by('-idPeriodo')
	contexto= {'periodo':periodo, 'kardex':kardex}
	return render(request, 'inventario/listPeriodos.html',contexto)




#metodo en caso de una transaccion de tipo compra
def compra(transaccionInventario):
	#Busqueda del producto para modificar su existencia
	producto = Producto.objects.get(idProducto= transaccionInventario.producto.idProducto)	
	#Busqueda del kardex
	kardex = Kardex.objects.get(producto=transaccionInventario.producto)
	#Busqueda de su ultimo periodo
	periodo = Periodo.objects.filter(kardex=kardex).last()
	#General
	lpFecha = transaccionInventario.fecha
	lpFactura = transaccionInventario.factura
	lpTipo = transaccionInventario.tipo
	lpValorUnitario = transaccionInventario.valorUnitario
	lpPeriodo = periodo
	#Entradas
	lpCantidadEntrada = transaccionInventario.cantidadTransaccion
	lpValorEntrada = lpValorUnitario * lpCantidadEntrada
	#Salidas
	lpValorSalida = 0
	lpCantidadSalida = 0
	#Existencias
	#Validaciones si no hay lineas de Periodo anteriores
	if LineaPeriodo.objects.filter(periodo=periodo).exists()==True:
		lpAnterior = LineaPeriodo.objects.filter(periodo=periodo).last()
		lpCantidadExistencia = int(lpAnterior.cantidadExistencia) + lpCantidadEntrada
		lpValorExistencia = float(lpAnterior.valorExistencia) + float(lpValorEntrada)
	else :	
		lpCantidadExistencia= lpCantidadEntrada
		lpValorExistencia= lpValorEntrada	
	#Comprobacion
	lpCantidadSobrante = lpCantidadEntrada
	lpComprobacion = lpCantidadSobrante * lpValorUnitario
		#Guardando la nueva linea del periodo
	lineaperiodo = LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida, cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,comprobacion = lpComprobacion, compraAsociada=0,periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
	lineaperiodo.save()
	producto.existencias= lineaperiodo.cantidadExistencia
	producto.save()



#metodo en caso de transaccion de tipo Venta
def venta(transaccionInventario):
#Busqueda del producto para modificar su existencia
	producto = Producto.objects.get(idProducto= transaccionInventario.producto.idProducto)		
#Busqueda del kardex
	kardex = Kardex.objects.get(producto=transaccionInventario.producto)
#Busqueda de su ultimo periodo
	periodo = Periodo.objects.filter(kardex=kardex).last()
#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=periodo).last()
#Primera compra cuya cantidad sobrante sea >0
	lcPrimera = LineaPeriodo.objects.filter(Q(periodo=periodo, cantidadSobrante__gt=0, tipoTransaccion='C')|Q(periodo=periodo, cantidadSobrante__gt=0, tipoTransaccion='I')).first()
#logica 
	#General
	lpFecha= transaccionInventario.fecha
	lpFactura= transaccionInventario.factura
	lpTipo= transaccionInventario.tipo
	lpValorUnitario= lcPrimera.valorUnitario
	lpPeriodo= periodo
	#Entrada
	lpCantidadEntrada=0
	lpValorEntrada= 0
	#Comprobacion
	lpCantidadSobrante= 0
	lpComprobacion= 0
	#Campo exclusivo para Ventas
	lpCompraAsociada= lcPrimera.idLineaPeriodo		
#Si la cantidad de venta es menor a la primera compra con con existencia mayor que 0
	if transaccionInventario.cantidadTransaccion<=lcPrimera.cantidadSobrante:		
		#Salidas	
		lpCantidadSalida=transaccionInventario.cantidadTransaccion
		lpValorSalida=lpValorUnitario * lpCantidadSalida
		#Existencias
		lpCantidadExistencia= int(lpAnterior.cantidadExistencia) - lpCantidadSalida		
		lpValorExistencia=float(lpAnterior.valorExistencia) - float(lpValorSalida)		
		#Creacion de la nueva linea del periodo
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    		cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    		valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    		cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
		lineaperiodo.save()
		#Cambiando la comprobacion de la compra que redujo cantidad sobrante
		lcPrimera.cantidadSobrante= int(lcPrimera.cantidadSobrante)- lpCantidadSalida
		lcPrimera.comprobacion= int(lcPrimera.cantidadSobrante)* float(lcPrimera.valorUnitario)
		lcPrimera.save()
		producto.existencias= lineaperiodo.cantidadExistencia
		producto.save()
	#Si la cantidad de venta es mayor a la primera compra con con existencia mayor que 0	
	else :
		#Salida		
		lpCantidadSalida= lcPrimera.cantidadSobrante
		lpValorSalida=lpValorUnitario * lpCantidadSalida
		#Existencias
		lpCantidadExistencia= int(lpAnterior.cantidadExistencia) - lpCantidadSalida	
		lpValorExistencia=float(lpAnterior.valorExistencia) - lpValorSalida
		#Creacion de la nueva linea de periodo
		lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    		cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    		valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    		cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
		lineaperiodo.save()
		#Guardando comprobacion de la compra afectada
		lcPrimera.cantidadSobrante= 0
		lcPrimera.comprobacion= 0
		lcPrimera.save()
		producto.existencias= lineaperiodo.cantidadExistencia
		producto.save()
		#cantidad de productos que falta por vender	
		ventaFaltantante= transaccionInventario.cantidadTransaccion- lpCantidadSalida
		while ventaFaltantante>0:
			ventaFaltantante = ventaRepeticion(ventaFaltantante, kardex, periodo, lpFecha,lpFactura, lpTipo, producto, transaccionInventario)

    	

#Metodo para crear multiples lineas de ventas si esta se hace de diferentes lineas de compra
def ventaRepeticion(ventafaltantante, Kardex, Periodo, Fecha, Factura, Tipo, producto,transaccionInventario):
	producto1=producto
	#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=Periodo).last()
#Primera compra cuya cantidad sobrante sea >0
	lcPrimera = LineaPeriodo.objects.filter(Q(periodo=Periodo, cantidadSobrante__gt=0, tipoTransaccion='C')|Q(periodo=Periodo, cantidadSobrante__gt=0, tipoTransaccion='I')).first()
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
	if ventafaltantante<=lcPrimera.cantidadSobrante:		
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
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
		lineaperiodo.save()
		#Cambiando la comprobacion de la compra que redujo cantidad sobrante
		lcPrimera.cantidadSobrante= lcPrimera.cantidadSobrante- lpCantidadSalida
		lcPrimera.comprobacion= lcPrimera.cantidadSobrante* lcPrimera.valorUnitario
		lcPrimera.save()
		producto1.existencias= lineaperiodo.cantidadExistencia
		producto1.save()
		ventaFaltantanteNueva=0
	else :
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
    		comprobacion = lpComprobacion, compraAsociada=lpCompraAsociada, periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
		lineaperiodo.save()
		#Cambiar comprobacion de la compra afectada
		lcPrimera.cantidadSobrante= lcPrimera.cantidadSobrante- lpCantidadSalida
		lcPrimera.comprobacion= lcPrimera.cantidadSobrante* lcPrimera.valorUnitario
		lcPrimera.save()
		producto1.existencias= lineaperiodo.cantidadExistencia
		producto1.save()
		ventaFaltantanteNueva = ventafaltantante- lpCantidadSalida  
	return ventaFaltantanteNueva

def devolucionCompra(transaccionInventario):
	#validacion factura, y que la devolucion sea menoro igual a la cantidad en la compra

#Busqueda del producto para modificar su existencia
	producto = Producto.objects.get(idProducto= transaccionInventario.producto.idProducto)
	#Busqueda del kardex
	kardex = Kardex.objects.get(producto=transaccionInventario.producto)
	#Busqueda de su ultimo periodo
	periodo = Periodo.objects.filter(kardex=kardex).last()
	#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpAnterior = LineaPeriodo.objects.filter(periodo=periodo).last()
	#Busqueda de la compra asociada con la devolucion
	lcDevolucion = LineaPeriodo.objects.get(Q(periodo=periodo, tipoTransaccion='C', factura= transaccionInventario.factura)|Q(periodo=periodo, tipoTransaccion='I', factura= transaccionInventario.factura))
	#General
	lpFecha = transaccionInventario.fecha
	lpFactura = transaccionInventario.factura
	lpTipo = transaccionInventario.tipo
	lpValorUnitario = lcDevolucion.valorUnitario
	lpPeriodo = periodo
	#Entradas
	lpCantidadEntrada = -transaccionInventario.cantidadTransaccion
	lpValorEntrada = float(lpValorUnitario * lpCantidadEntrada)
	#Salidas
	lpValorSalida = 0
	lpCantidadSalida = 0
	#Existencias
	lpCantidadExistencia = int(lpAnterior.cantidadExistencia) + lpCantidadEntrada
	lpValorExistencia = float(lpAnterior.valorExistencia) + lpValorEntrada
	#Comprobacion
	lpCantidadSobrante = 0
	lpComprobacion = 0
		#Guardando la nueva linea del periodo
	lineaperiodo = LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, cantidadSobrante= lpCantidadSobrante, valorUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida, cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,comprobacion = lpComprobacion, compraAsociada=0,periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
	lineaperiodo.save()
	#Modificacion de la compra afectada
	lcDevolucion.cantidadSobrante= int(lcDevolucion.cantidadSobrante) + lpCantidadEntrada
	lcDevolucion.comprobacion= int(lcDevolucion.cantidadSobrante)* float(lcDevolucion.valorUnitario)
	lcDevolucion.save()
	producto.existencias= lineaperiodo.cantidadExistencia
	producto.save()



def devolucionVenta(transaccionInventario):
	
	#validacion factura, y que la devolucion sea menoro igual a la cantidad en la compra

#Busqueda del producto para modificar su existencia
	producto = Producto.objects.get(idProducto= transaccionInventario.producto.idProducto)
	#Busqueda del kardex
	kardex = Kardex.objects.get(producto=transaccionInventario.producto)
	#Busqueda de su ultimo periodo
	periodo = Periodo.objects.filter(kardex=kardex).last()	
	#Busqueda de las ventas asociadas con la devolucion
	ventas= LineaPeriodo.objects.filter(periodo=periodo, tipoTransaccion='V', factura= transaccionInventario.factura).order_by('idLineaPeriodo')
	devolucionFaltante=transaccionInventario.cantidadTransaccion
	for venta in ventas:
		if devolucionFaltante>0:
			#Busqueda de ultima lineaPeriodo para el periodo encontrado
			lpAnterior = LineaPeriodo.objects.filter(periodo=periodo).last()
			compraAsociada = LineaPeriodo.objects.get(idLineaPeriodo= venta.compraAsociada)
			#General
			lpFecha = transaccionInventario.fecha
			lpFactura = transaccionInventario.factura
			lpTipo = transaccionInventario.tipo
			lpValorUnitario = compraAsociada.valorUnitario
			lpPeriodo = periodo
			#Entradas
			lpCantidadEntrada = 0
			lpValorEntrada = 0
			if devolucionFaltante<= venta.cantidadSalida:
				#Salidas
				lpCantidadSalida = devolucionFaltante*(-1)
				lpValorSalida = float(lpValorUnitario * lpCantidadSalida)
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
    			comprobacion = lpComprobacion, compraAsociada=0, periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
				lineaperiodo.save()
				#Actualizando comprobacion de compra Asociada
				compraAsociada.cantidadSobrante= int(compraAsociada.cantidadSobrante) - lpCantidadSalida
				compraAsociada.comprobacion= int(compraAsociada.cantidadSobrante)* float(compraAsociada.valorUnitario)
				compraAsociada.save()
				producto.existencias= lineaperiodo.cantidadExistencia
				producto.save()
				devolucionFaltante=0
			else :
				#Salidas
				lpCantidadSalida = venta.cantidadSalida*(-1)
				lpValorSalida = lpValorUnitario * lpCantidadSalida
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
    			comprobacion = lpComprobacion, compraAsociada=0, periodo= lpPeriodo, transaccionInvAsociada=transaccionInventario)
				lineaperiodo.save()
				#Actualizando comprobacion de compra Asociada
				compraAsociada.cantidadSobrante= compraAsociada.cantidadSobrante - lpCantidadSalida
				compraAsociada.comprobacion= compraAsociada.cantidadSobrante* compraAsociada.valorUnitario
				compraAsociada.save()
				producto.existencias= lineaperiodo.cantidadExistencia
				producto.save()
				devolucionFaltante= devolucionFaltante + lpCantidadSalida




def cierreContableKardex(fechaFinal):
	productos = Producto.objects.filter(estado='Activo')
	for producto in productos:
		kardex = Kardex.objects.get(producto=producto)
		#filtrando el ultimo periodo de cada Kardex y asignando su saldo y existencia final
		periodo = Periodo.objects.filter(kardex=kardex).last()
		#La fecha deberia ser cuando den click en cierre contable, pero por facilidad sera cuando decidamos
		fecha = fechaFinal
		periodo.fechaFinal = fecha
		lpUltima = LineaPeriodo.objects.filter(periodo=periodo).last()
		periodo.existenciaFinal= lpUltima.cantidadExistencia
		periodo.saldoFinal= lpUltima.valorExistencia
		periodo.save()
		#Creando el nuevo periodo para cada Kardex
		fecha= datetime.datetime.strptime(fecha, "%Y-%m-%d")
		diaSiguiente= fecha + datetime.timedelta(days=1)
		periodoNuevo= Periodo(fechaInicio = diaSiguiente ,existenciaFinal=0,saldoFinal =0,kardex= kardex)
		periodoNuevo.save()
		#productos sobrantes de periodo anterior pasan a inventario inicial del nuevo Periodo
		existenciasSobrantes= LineaPeriodo.objects.filter(Q(tipoTransaccion='C', periodo=periodo, cantidadSobrante__gt=0)| Q(tipoTransaccion='I', periodo=periodo, cantidadSobrante__gt=0)).order_by('idLineaPeriodo')
		for existencia in existenciasSobrantes:							
			#valores de entrada
			sobrante= existencia.cantidadSobrante			
			valorEntrada = sobrante* existencia.valorUnitario
			transInv=existencia.transaccionInvAsociada
			comprobacion= sobrante*existencia.valorUnitario
			#Validaciones si no hay lineas de Periodo anteriores
			if LineaPeriodo.objects.filter(periodo=periodoNuevo).exists()==True:
				lpAnterior = LineaPeriodo.objects.filter(periodo=periodoNuevo).last()
				cantidadExistencia = lpAnterior.cantidadExistencia + sobrante
				valorExistencia = lpAnterior.valorExistencia + valorEntrada
			else :	
				cantidadExistencia= sobrante
				valorExistencia= valorEntrada
			invInicial= LineaPeriodo(factura =existencia.factura ,fecha=diaSiguiente,tipoTransaccion ='I',valorUnitario=existencia.valorUnitario,periodo=periodoNuevo,cantidadEntrada =sobrante,valorEntrada =valorEntrada,cantidadSalida =0,valorSalida =0,cantidadExistencia =cantidadExistencia,valorExistencia =valorExistencia,comprobacion = comprobacion,cantidadSobrante=sobrante,compraAsociada=0,transaccionInvAsociada=transInv)
			invInicial.save()
			


