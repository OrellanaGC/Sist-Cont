from django.shortcuts import render, redirect
from datetime import datetime
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from apps.cuenta.models import Cuenta
from apps.producto.models import Producto
from apps.transaccion.models import Transaccion

# Create your views here.
def resumenPartida(request):
    data = {'cuentas' : getCuentas() , 'transacciones' : getTransacciones()}
    return render(request, 'partida/partidas.html', data)


def nuevaPartida(request):
    productos = Producto.objects.filter(estado='A')
    transacciones = Transaccion.objects.all().values()
    data = {'cuentas' : getCuentas(), 'productos' : productos, 'transacciones' : transacciones}
    return render(request, 'partida/partida.html', data)

def agregarTransaccion(request):
    mensaje = "Transacción agregada"
    if request.method == 'POST':
        detalle = request.POST['detalle']
        monto = request.POST['monto']
        fechaStr = datetime.strptime(request.POST['fecha'], '%d/%m/%Y')
        fecha = fecha.strftime('%Y-%m-%d')
        tipo = request.POST['tipo']
        cuenta = Cuenta.objects.get(idCuenta=request.POST['idCuenta'])
        #Solo se agrega a las transacciones
        transaccion = Transaccion(detalle=detalle, monto=monto, fecha=fecha, cuenta=cuenta, tipo=tipo)
        transaccion.save()
    data = {'mensaje' : mensaje, 'cuentas' : getCuentas(), 'transacciones' : getTransacciones(), 'productos' : getProductos()}
    return render(request, 'partida/partida.html', data)

def eliminarTransaccion(request, idTransaccion):
    if request.method == 'POST':
        transaccion = Transaccion.objects.get(idTransaccion=idTransaccion)
        transaccion.delete()
        transacciones = getTransacciones()
        data = {'mensaje' : mensaje, 'transacciones' : getTransacciones(), 'productos' : getProductos()}
    return render(request, 'partida/partida.html', data)

def getTransacciones():
    transacciones = Transaccion.objects.all()
    return transacciones

def getProductos():
    productos = Productos.objects.all()
    return productos

def getCuentas():
    cuentas = Cuenta.objects.filter(estado='A')
    return cuentas