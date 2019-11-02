from django.shortcuts import render, redirect
from apps.cuenta.models import Cuenta

# Create your views here.
def resumenCuenta(request):
    cuentas = Cuenta.objects.filter(estado='A')
    data = {'cuentas' : cuentas}
    return render(request, 'cuenta/cuentas.html', data)

def nuevaCuenta(request):
    cuentas = Cuenta.objects.filter(estado='A')
    if request.method == 'POST':
        if request.POST["cuentaPadre"] > 0:
            cuenta = Cuenta(codigoCuenta=request.POST["codigo"], nombre=request.POST["nombre"], saldo=request.POST["saldo"], modificaInventario=request.POST["modificaInventario"], cuentaPadre_id=request.POST["cuentaPadre"], estado=request.POST["estado"], estadoCuenta=request.POST["estadoCuenta"], tipo=request.POST["tipo"])
            cuenta.save()
        else:
            cuenta = Cuenta(codigoCuenta=request.POST["codigo"], nombre=request.POST["nombre"], saldo=request.POST["saldo"], modificaInventario=request.POST["modificaInventario"], estado=request.POST["estado"], estadoCuenta=request.POST["estadoCuenta"], tipo=request.POST["tipo"])
            cuenta.save()
    data = {'cuentas' : cuentas}
    return render(request, 'cuenta/cuenta.html', data)

def modificarCuenta(request, idCuenta):
    cuenta = Cuenta.objects.get(idCuenta=idCuenta)
    data = {'cuenta': cuenta}
    if request.method == 'POST':
        cuenta = Cuenta.objects.get(idCuenta=idCuenta)
        cuenta.codigoCuenta = request.POST["codigo"]
        cuenta.nombre = request.POST["nombre"]
        cuenta.saldo = request.POST["saldo"]
        cuenta.modificaInventario = request.POST["modificaInventario"]
        if request.POST["cuentaPadre"] > 0:
            cuenta.cuantaPadre_id = request.POST["cuentaPadre"]
        cuenta.estado = request.POST["estado"]
        cuenta.estadoCuenta = request.POST["estadoCuenta"]
        cuenta.tipo = request.POST["tipo"]
        cuenta.save()
    return render(request, 'cuenta/cuenta.html', data)

def eliminarCuenta(request, idCuenta):
    cuenta = Cuenta.objects.get(idCuenta=idCuenta)
    cuenta.delete()
    return redirect('resumenCuenta')
