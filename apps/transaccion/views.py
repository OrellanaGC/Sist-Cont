from django.shortcuts import render, redirect
from datetime import datetime
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from apps.cuenta.models import Cuenta
from apps.producto.models import Producto
from apps.transaccion.models import Transaccion
import json

# Create your views here.
def resumenPartida(request):
    if request.method == 'POST':
        fechac = request.POST['MP']
        fecha = datetime.strptime(fechac,  '%Y-%m')
        fecha1 = fecha.year
        fecha2 = fecha.month
        Trans = Transaccion.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month)
    else:
        today = datetime.today()
        Trans = Transaccion.objects.filter(fecha__year= today.year, fecha__month=today.month)
    data = {'cuentas' : getCuentas() , 'transacciones' : Trans}
    return render(request, 'partida/partidas.html', data)

def cargarXCP(request, cuentaPadre):
    if request.method == 'POST': # caso que este fecha especifica
        fechac = request.POST['MP']
        fecha = datetime.strptime(fechac,  '%Y-%m')
        fecha1 = fecha.year
        fecha2 = fecha.month
        Trans = Transaccion.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, cuenta__cuentaPadre__codigoCuenta = cuentaPadre)
    else: #Agregar fecha actual
        Trans = Transaccion.objects.filter(cuenta__cuentaPadre__codigoCuenta = cuentaPadre).order_by('fecha')    
    data = {'cuentas' : getCuentas() , 'transacciones' : Trans, 'cuentaPadre' : cuentaPadre}
    return render(request, 'partida/partidas.html', data)

def nuevaPartida(request):
    idsCtas = ''
    txtAenv = None    
    productos = Producto.objects.filter(estado='A')
    cuentasLst = getCuentasOrd()
    cuentasModInv = []
    cuentasModInvObj = Cuenta.objects.filter(modificaInventario=True)
    for c in cuentasModInvObj:
        cuentasModInv.append(c.idCuenta)
    transacciones = None   
    cuentasModInv = json.dumps(cuentasModInv)
    #agregando
    ok = 0
    if request.method == 'POST':    
        idsCtas = request.POST['hidId']
        detalle = request.POST['detalle']
        monto = request.POST['monto']
        fechaStr = datetime.strptime(request.POST['fechaE'], '%Y-%m-%d')
        fecha = fechaStr.strftime('%Y-%m-%d')
        tipo = request.POST['tipo']
        cuenta = Cuenta.objects.get(idCuenta=request.POST['seleCuenta'])        
        transaccion = Transaccion(detalle=detalle, monto=monto, fecha=fecha, cuenta=cuenta, tipo=tipo)
        transaccion.save()        
        if idsCtas != '':
            idsCtas += "-" + str(transaccion.idTransaccion)
        else:
            idsCtas += str(transaccion.idTransaccion)
        #cargando transacciones del ambito
        transacciones = []
        idsCtas = idsCtas.split('-');
        suma = 0
        txtAenv = ''
        for c in idsCtas:
            if txtAenv == '':
                txtAenv += str(c)
            else:
                txtAenv += '-' + str(c)
            t = Transaccion.objects.get(idTransaccion=c)
            transacciones.append(t)
            if t.tipo == 'C':
                suma += t.monto
            else:
                suma -= t.monto        
        if suma == 0:
            ok = 1
    data = {'cuentas' : cuentasLst, 'productos' : productos, 'transacciones' : transacciones, 'cuentasModInv' : cuentasModInv, 'idsCtas' : txtAenv, 'trans' : transacciones, 'ok' : ok}
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
    transacciones = Transaccion.objects.all().order_by('fecha')
    return transacciones

def getProductos():
    productos = Producto.objects.all()
    return productos

def getCuentas():
    cuentas = Cuenta.objects.filter(estado='A')
    return cuentas

def getCuentasOrd(): #Cuentas ordenadas de acuerdo a su padre
    cuentas = [*Cuenta.objects.filter(estado='A',codigoCuenta__startswith='1'),
    *Cuenta.objects.filter(estado='A',codigoCuenta__startswith='2'),
    *Cuenta.objects.filter(estado='A',codigoCuenta__startswith='3'),
    *Cuenta.objects.filter(estado='A',codigoCuenta__startswith='4'),
    *Cuenta.objects.filter(estado='A',codigoCuenta__startswith='5'),
    *Cuenta.objects.filter(estado='A',codigoCuenta__startswith='6'),
    *Cuenta.objects.filter(estado='A',codigoCuenta__startswith='7')]
    return cuentas