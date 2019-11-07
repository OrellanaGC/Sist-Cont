from django.shortcuts import render, redirect
from apps.empresa.models import Empresa
import re

# Create your views here.
def resumenEmpresa(request):
    empresa = Empresa.objects.first()
    data = {'empresa' : empresa, 'editar': False}
    return render(request, 'empresa/empresa.html', data)

def guardarDatos(request):
    empresa = Empresa.objects.first()
    errores = set()
    if request.method == 'POST':
        print("entrando post")
        if Empresa.objects.count() > 0:
            empresa = Empresa.objects.first()
            empresa.nombre = request.POST["nombre"]
            empresa.nombreContribuyente = request.POST["contribuyente"]
            empresa.nit = request.POST["nit"]
            empresa.nrc = request.POST["nrc"]
            empresa.giro = request.POST["giro"]
            empresa.save()
            print("entrando if")
            print('save')
            return redirect('resumenEmpresa')
        else:
            print("entrando else")
            errores = validarDatos(request.POST["nit"], request.POST["nrc"], request.POST["nombre"], request.POST["contribuyente"], request.POST["giro"])
            if len(errores) == 0:
                empresaNueva = Empresa(nombre=request.POST["nombre"], nombreContribuyente=request.POST["contribuyente"], nit=request.POST["nit"], nrc=request.POST["nrc"], giro=request.POST["giro"])
                empresaNueva.save()
                print('save')
            return redirect('resumenEmpresa', data)
    data = {'empresa' : empresa, 'editar': True, 'errores' : errores}
    return render(request, 'empresa/empresa.html', data)

def validarDatos(nit, nrc, nombre, contribuyente, giro):
    errores = set()
    if(not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$", giro)):
        errores.add('Giro de la empresa inválido')
    if(not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$", nombre)):
        errores.add('Nombre de empresa inválido')
    if(not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$", nombre)):
        errores.add('Nombre de contribuyente inválido')
    if(not re.match("^[0-9]{4}-[0-9]{6}-[0-9]{3}-[0-9]$", nit)):
        errores.add("NIT inválido")
    if(not re.match("^[0-9]{6}-[0-9]{1}$", nrc)):
        errores.add("NRC inválido")
    return errores