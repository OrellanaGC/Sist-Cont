from django.shortcuts import render
from django.views.generic.list import ListView
#from django.views.generic import TemplateView
from apps.kardex.models import Kardex, Periodo, LineaPeriodo
from apps.transaccionInventario.models import *


def inventario(request):
    return render(request, 'inventario/inventario.html')

class ListaKardex(ListView):
	model= Kardex
	template_name='inventario/inventario.html'

#def ListaInventario(self):
'''class ListarProductos(ListView):
	model= Producto
	template_name='inventario/inventario.html
class ListaKardex(ListView):
	template_name='inventario/inventario.html'
	context_object_name = 'kardex_list'
	queryset = Producto.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(ListaKardex, self).get_context_data(**kwargs)
		context['kardex'] = Kardex.objects.all()
		context['productos'] = self.queryset
		return context'''


"""
#metoco en caso de una transaccion de tipo compra
def compra(transaccionInventario):
	transInventario= TransaccionInventario(fecha =request.POST['fecha'], cantidadComprada =request.POST['cantidad'], 
	costoUnitario =request.POST['costoUnitario'], factura =request.POST['factura'], 
	tipo =request.POST['tipo'], producto =request.POST['producto'])
#Busqueda del kardex
	Kardex = Kardex.objects.get(producto=transaccionInventario.producto)
#Busqueda de su ultimo periodo
	Periodo = Periodo.objects.get(kardex=Kardex).last()
#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpA = lineaPeriodo.objects.get(periodo=Periodo).last()
#Asignacion de valor y creacion de nueva lineaPeriodo
	lpFecha= request.POST['fecha']
	lpFactura=request.POST['factura']
	lpTipo=request.POST['tipo']	
	lpValorUnitario=request.POST['valorUnitario']
	lpCantidadEntrada=request.POST['cantidad']
	lpCantidadSalida=0
	lpCantidadExistencia= lpA.cantidadExistencia + lpCantidadEntrada
	lpValorEntrada= lpValorUnitario * lpCantidadEntrada
	lpValorSalida=0
	lpValorExistencia=lpA.valorExistencia + lpValorEntrada
	lpPeriodo= Periodo
	lpCantidadSobrante= lpCantidadEntrada
	lpComprobacion= lpCantidadSobrante * lpValorUnitario
	lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    cantidadSobrante= lpCantidadSobrante, costoUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    comprobacion = lpComprobacion, periodo= Periodo)
    lineaperiodo.save()

#metodo en caso de transaccion de tipo Venta
def venta(request):
	transInventario= TransaccionInventario(fecha =request.POST['fecha'], cantidadComprada =request.POST['cantidad'], 
	costoUnitario =request.POST['costoUnitario'], factura =request.POST['factura'], 
	tipo =request.POST['tipo'], producto =request.POST['producto'])
#Busqueda del kardex
	Kardex = Kardex.objects.get(producto=transaccionInventario.producto)
#Busqueda de su ultimo periodo
	Periodo = Periodo.objects.get(kardex=Kardex).last()
#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpA = lineaPeriodo.objects.get(periodo=Periodo).last()
#Primera compra cuya cantidad sobrante sea >0
	lcp = LineaPeriodo.objects.get(periodo=Periodo, cantidadSobrante>0).first()
#logica 
	lpFecha= request.POST['fecha']
	lpFactura=request.POST['factura']
	lpTipo=request.POST['tipo']	
	lpCantidadEntrada=0
	lpValorEntrada= 0
	lpCantidadSobrante= 0
	lpComprobacion= 0
	lpPeriodo= Periodo	
#Si la cantidad de venta es mayor a la primera compra con con existencia mayor que 0
if request.cantidad<lcp.cantidadSobrante:		
	lpValorUnitario= lcp.costoUnitario
	lpCantidadSalida=request.POST['cantidad']
	lpCantidadExistencia= lpA.cantidadExistencia - lpCantidadSalida	
	lpValorSalida=lpValorUnitario * lpCantidadSalida
	lpValorExistencia=lpA.valorExistencia - lpValorSalida	
	lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    cantidadSobrante= lpCantidadSobrante, costoUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    comprobacion = lpComprobacion, periodo= Periodo)
    lineaperiodo.save()
    lcp.cantidadSobrante= lcp.cantidadSobrante- lpValorSalida
    lcp.comprobacion= lcp.cantidadSobrante* lcp.valorUnitario
    lcp.save()
#Si la cantidad de venta es menor a la primera compra con con existencia mayor que 0
if request.cantidad>lcp.cantidadSobrante:
	lpValorUnitario= lcp.costoUnitario	
	lpCantidadSalida= lcp.cantidadSobrante
	lpCantidadExistencia= lpA.cantidadExistencia - lpCantidadSalida	
	lpValorSalida=lpValorUnitario * lpCantidadSalida
	lpValorExistencia=lpA.valorExistencia - lpValorSalida
	lpPeriodo= Periodo	
	lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    cantidadSobrante= lpCantidadSobrante, costoUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    comprobacion = lpComprobacion, periodo= Periodo)
    lineaperiodo.save()
    lcp.cantidadSobrante= 0
    lcp.comprobacion= 0
    lcp.save()	
    cantidadExpress= lpCantidadSalida- request.POST["cantidad"]
    while cantidadExpress>0:
    	





#Metodo para crear multiples lineas de ventas si esta se hace de diferentes lineas de compra
def ventaRepeticion(request, Kardex, Periodo):
	#Busqueda de ultima lineaPeriodo para el periodo encontrado
	lpA = lineaPeriodo.objects.get(periodo=Periodo).last()
#Primera compra cuya cantidad sobrante sea >0
	lcp = LineaPeriodo.objects.get(periodo=Periodo, cantidadSobrante>0, tipo=compra).first()
#Repeticion de logica de venta
	lpFecha= argumentolP.fecha
	lpFactura= argumentolP.factura
	lpTipo= argumentolP.tipoTransaccion	
	lpValorUnitario= lcp.costoUnitario
	lpCantidadEntrada=0
	lpCantidadSalida= lcp.cantidadSobrante
	lpCantidadExistencia= lpA.cantidadExistencia - lpCantidadSalida
	lpValorEntrada= 0
	lpValorSalida=lpValorUnitario * lpCantidadSalida
	lpValorExistencia=lpA.valorExistencia - lpValorSalida
	lpPeriodo= Periodo
	lpCantidadSobrante= 0
	lpComprobacion= 0
	lineaperiodo= LineaPeriodo(factura = lpFactura, fecha=lpFecha, tipoTransaccion = lpTipo, 
    cantidadSobrante= lpCantidadSobrante, costoUnitario= lpValorUnitario, cantidadEntrada =lpCantidadEntrada, 
    valorEntrada = lpValorEntrada, cantidadSalida = lpCantidadSalida, valorSalida = lpValorSalida,
    cantidadExistencia = lpCantidadExistencia, valorExistencia = lpValorExistencia,
    comprobacion = lpComprobacion, periodo= Periodo)
    lineaperiodo.save()
    lcp.cantidadSobrante= 0
    lcp.comprobacion= 0
    lcp.save()	
    cantidadExpress= lpCantidadSalida- request.POST["cantidad"] """


	