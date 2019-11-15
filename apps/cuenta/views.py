from django.shortcuts import render, redirect
from apps.cuenta.models import Cuenta
from django.contrib.auth.decorators import login_required
import re

# Create your views here.
@login_required
def resumenCuenta(request):
    cuentas = Cuenta.objects.filter(estado='A')
    data = {'cuentas' : cuentas}
    return render(request, 'cuenta/cuentas.html', data)

@login_required
def nuevaCuenta(request):
    cuentas = Cuenta.objects.filter(estado='A')
    inventario = False
    errores = set()
    if request.method == 'POST':
        errores = validarDatos(request.POST["nombre"], request.POST["cuentaPadre"], request.POST["codigo"], request.POST["saldo"], request.POST["estadoCuenta"], request.POST["estado"], request.POST["tipoCuenta"])
        #if len(errores) == 0:
        if int(request.POST["cuentaPadre"]) > 0:
            if 'inventario' in request.POST:
                inventario = True
            else:
                inventario = False
            cuentaPadre = Cuenta.objects.get(idCuenta=request.POST["cuentaPadre"])
            #cuentasHijo = Cuenta.objects.filter(cuentaPadre_id=cuentaPadre.idCuenta)
            #saldoHijos = float(request.POST["saldo"])
            #for cuentaHijo in cuentasHijo:
            #    saldoHijos += float(cuentaHijo.saldo)
            #if saldoHijos <= cuentaPadre.saldo:
            cuenta = Cuenta(codigoCuenta=cuentaPadre.codigoCuenta + request.POST["codigo"], nombre=request.POST["nombre"], saldo=request.POST["saldo"], modificaInventario=inventario, cuentaPadre_id=request.POST["cuentaPadre"], estado=request.POST["estado"], estadoCuenta=request.POST["estadoCuenta"], tipo=cuentaPadre.tipo)
            cuenta.save()
            #else:
            #    errores.add("Error al guardar")
        else:
            cuenta = Cuenta(codigoCuenta=request.POST["codigo"], nombre=request.POST["nombre"], saldo=request.POST["saldo"], modificaInventario=inventario, estado=request.POST["estado"], estadoCuenta=request.POST["estadoCuenta"], tipo=request.POST["tipoCuenta"])
            cuenta.save()
    data = {'cuentas' : cuentas, 'errores' : errores, 'editando': False}
    return render(request, 'cuenta/cuenta.html', data)

@login_required
def modificarCuenta(request, idCuenta):
    cuenta = Cuenta.objects.get(idCuenta=idCuenta)
    print(cuenta.tipo)
    data = {'cuenta': cuenta, 'editando': True}
    if request.method == 'POST':
        cuentaPadre = Cuenta.objects.get(idCuenta=request.POST["cuentaPadre"])
        cuentasHijo = Cuenta.objects.filter(cuentaPadre_id=cuentaPadre.idCuenta)
        saldoHijos = float(request.POST["saldo"])
        for cuentaHijo in cuentasHijo:
            saldoHijos += float(cuentaHijo.saldo)
        if saldoHijos <= cuentaPadre.saldo:
            cuenta = Cuenta.objects.get(idCuenta=idCuenta)
            cuenta.codigoCuenta = request.POST["codigo"]
            cuenta.nombre = request.POST["nombre"]
            cuenta.saldo = request.POST["saldo"]
            cuenta.modificaInventario = request.POST["modificaInventario"]
            if int(request.POST["cuentaPadre"]) > 0:
                cuenta.cuantaPadre_id = request.POST["cuentaPadre"]
            cuenta.estado = request.POST["estado"]
            cuenta.estadoCuenta = request.POST["estadoCuenta"]
            cuenta.tipo = request.POST["tipo"]
            cuenta.save()
        else:
            print("Error al modificar")
    return render(request, 'cuenta/cuenta.html', data)

@login_required
def eliminarCuenta(request, idCuenta):
    cuenta = Cuenta.objects.get(idCuenta=idCuenta)
    cuenta.delete()
    return redirect('resumenCuenta')

def validarDatos(nombre, cuentaPadre, codigoCuenta, saldo, estadoCuenta, tipo, estado):
    errores = set()
    if(not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$", nombre)):
        errores.add('Nombre de cuenta inválido')
    if (not re.match("^[0-9]*$", cuentaPadre) or cuentaPadre == ""):
        errores.add("Cuenta padre inválida")
    if (not re.match("^[0-9]*$", codigoCuenta)):
        errores.add("Código de cuenta inválido")
    if (not re.match("^[A|D|S]$", estadoCuenta)):
        errores.add("Estado de cuenta inválido")
    if (not re.match("^[D|H]$", tipo)):
        errores.add("Tipo de cuenta inválido")
    if (not re.match("^[A|D]", estado)):
        errores.add("Estado de cuenta inválido")
    if(not re.match("^([-+]?[0-9]*\.?[0-9]+)$", saldo)):
        errores.add("Saldo de cuenta inválido")
    return errores
