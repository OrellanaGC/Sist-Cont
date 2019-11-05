from django.shortcuts import render, redirect
from apps.cuenta.models import Cuenta

# Create your views here.
def resumenCuenta(request):
    cuentas = Cuenta.objects.filter(estado='A')
    data = {'cuentas' : cuentas}
    return render(request, 'cuenta/cuentas.html', data)

def nuevaCuenta(request):
    cuentas = Cuenta.objects.filter(estado='A')
    inventario = False
    if 'inventario' in request.POST:
        inventario = True
    else:
        inventario = False
    if request.method == 'POST':
        if int(request.POST["cuentaPadre"]) > 0:
            cuentaPadre = Cuenta.objects.get(idCuenta=request.POST["cuentaPadre"])
            cuentasHijo = Cuenta.objects.filter(cuentaPadre_id=cuentaPadre.idCuenta)
            saldoHijos = float(request.POST["saldo"])
            for cuentaHijo in cuentasHijo:
                saldoHijos += float(cuentaHijo.saldo)
            if saldoHijos <= cuentaPadre.saldo:
                cuenta = Cuenta(codigoCuenta=cuentaPadre.codigoCuenta + request.POST["codigo"], nombre=request.POST["nombre"], saldo=request.POST["saldo"], modificaInventario=inventario, cuentaPadre_id=request.POST["cuentaPadre"], estado=request.POST["estado"], estadoCuenta=request.POST["estadoCuenta"], tipo=cuentaPadre.tipo)
                cuenta.save()
            else:
                print("Error al guardar")
        else:
            cuenta = Cuenta(codigoCuenta=request.POST["codigo"], nombre=request.POST["nombre"], saldo=request.POST["saldo"], modificaInventario=inventario, estado=request.POST["estado"], estadoCuenta=request.POST["estadoCuenta"], tipo=request.POST["tipoCuenta"])
            cuenta.save()
    data = {'cuentas' : cuentas}
    return render(request, 'cuenta/cuenta.html', data)

def modificarCuenta(request, idCuenta):
    cuenta = Cuenta.objects.get(idCuenta=idCuenta)
    data = {'cuenta': cuenta}
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

def eliminarCuenta(request, idCuenta):
    cuenta = Cuenta.objects.get(idCuenta=idCuenta)
    cuenta.delete()
    return redirect('resumenCuenta')