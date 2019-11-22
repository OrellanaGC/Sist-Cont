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
        Trans = Transaccion.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month).order_by('fecha')
    else:
        today = datetime.today()
        Trans = Transaccion.objects.filter(fecha__year= today.year, fecha__month=today.month).order_by('fecha')
    fechasMes = Trans.distinct('fecha')
    fechaDisplay = getFechasEncabezado(Trans, fechasMes)
    i = 0
    for t in Trans:        
        t.fecha = fechaDisplay[i]
        i += 1 
    data = {'cuentas' : getCuentas() , 'transacciones' : Trans, 'fechasMes' : fechaDisplay}
    return render(request, 'partida/partidas.html', data)

def cargarXCP(request, cuentaPadre):
    if request.method == 'POST': # caso que este fecha especifica
        fechac = request.POST['MP']
        fecha = datetime.strptime(fechac,  '%Y-%m')
        fecha1 = fecha.year
        fecha2 = fecha.month
        Trans = Transaccion.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, cuenta__cuentaPadre__codigoCuenta = cuentaPadre).order_by('fecha')
    else: #Agregar fecha actual
        Trans = Transaccion.objects.filter(cuenta__cuentaPadre__codigoCuenta = cuentaPadre).order_by('fecha')    
    #consiguiendo las fechas
    fechasMes = Trans.distinct('fecha')
    fechaDisplay = getFechasEncabezado(Trans, fechasMes)
    i = 0
    for t in Trans:        
        t.fecha = fechaDisplay[i]
        i += 1 
    data = {'cuentas' : getCuentas() , 'transacciones' : Trans, 'cuentaPadre' : cuentaPadre, 'fechasMes' : fechaDisplay}
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
        #validando si sale de saldada
        if cuenta.estadoCuenta == 'S' and float(monto) > 0:
            if tipo == 'C':
                cuenta.estadoCuenta = 'D'
            elif tipo == 'A':
                cuenta.estadoCuenta = 'A'
        #modificando la cuenta
        if tipo == 'C':            
            saldoP = cuenta.saldo + float(monto)
            cuenta.saldo = cuenta.saldo + float(monto)            
        else:
            cuenta.saldo = cuenta.saldo - float(monto)
            saldoP = cuenta.saldo - float(monto)
        cuenta.save()
        validarEstadoCta(cuenta.idCuenta)
        transaccion = Transaccion(detalle=detalle, monto=monto, fecha=fecha, cuenta=cuenta, tipo=tipo,saldoParcial = saldoP)
        transaccion.save()        
        #agregando transaccionInventario si lo indica
        if cuenta.modificaInventario == True:
            cantidad = request.POST['cantProd']
            nombre = request.POST['Prod']
            #kaaaaa
        if idsCtas != '':
            idsCtas += "-" + str(transaccion.idTransaccion)
        else:
            idsCtas += str(transaccion.idTransaccion)
        #cargando transacciones del ambito
        transacciones = []
        idsCtas = idsCtas.split('-')
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

def cancelarPartidaDoble(request,idsTransacc):
    idsCtas = str(idsTransacc).split('-')
    for c in idsCtas:
        t = Transaccion.objects.get(idTransaccion=c)
        cuenta = Cuenta.objects.get(idCuenta = t.cuenta_id)
        tipo = t.tipo
        monto = t.monto
        #modificando la cuenta
        if tipo == 'C':                        
            cuenta.saldo = cuenta.saldo - float(monto)
        else:
            cuenta.saldo = cuenta.saldo + float(monto)
        if cuenta.estadoCuenta == 'S':
            if tipo == 'C':
                cuenta.estadoCuenta = 'A'
            elif tipo == 'A':
                cuenta.estadoCuenta = 'D'
        cuenta.save()
        validarEstadoCta(cuenta.idCuenta)
        t.delete()
    return redirect('resumenPartida')

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

def getFechasEncabezado(Trans, fechasMes):
    fechaDisplay = []    
    i = 0
    j = 0
    agg = 0
    for fechas in fechasMes:
        incidencia = 0
        j = 0
        for transac in Trans:
            print('incidencia= ' + str(incidencia))
            print('agg= ' + str(agg))     
            if fechas.fecha == transac.fecha and incidencia == 0:
                incidencia = 1
                fechaDisplay.append(fechas.fecha)
                agg = 1
                print('agregue normal')
            elif fechas.fecha == transac.fecha and agg == 1:
                fechaDisplay.append('')
                print('agregue vacio')            
            j = j + 1
        agg = 0           
        i = i + 1
    return fechaDisplay

def validarEstadoCta(idCta):
    cuenta = Cuenta.objects.get(idCuenta = idCta) 
    saldo = cuenta.saldo
    estado = cuenta.estadoCuenta
    if saldo < 0 and estado == 'A':
        cuenta.estado = 'D'
        cuenta.saldo *= -1
    elif saldo < 0 and estado == 'D':
        cuenta.estado = 'A'
        cuenta.saldo *= -1
    elif saldo == 0:
        cuenta.estado = 'S'
    cuenta.save()
    return None