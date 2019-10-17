from django.shortcuts import render

# Create your views here.
def resumenCuenta(request):
    return render(request, 'cuenta/cuentas.html')
def nuevaCuenta(request):
    return render(request, 'cuenta/cuenta.html')
