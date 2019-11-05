from django.shortcuts import render, redirect
from apps.empresa.models import Empresa

# Create your views here.
def resumenEmpresa(request):
    empresa = Empresa.objects.first()
    data = {'empresa' : empresa, 'editar': False}
    return render(request, 'empresa/empresa.html', data)

def guardarDatos(request):
    empresa = Empresa.objects.first()
    data = {'empresa' : empresa, 'editar': True}
    if request.method == 'POST':
        print("entrando post")
        if Empresa.objects.count() > 0:
            empresa2 = Empresa.objects.first()
            empresa2.nombre = request.POST["nombre"]
            empresa2.nombreContribuyente = request.POST["contribuyente"]
            empresa2.nit = request.POST["nit"]
            empresa2.nrc = request.POST["nrc"]
            empresa2.giro = request.POST["giro"]
            empresa2.save()
            print("entrando if")
            print('save')
            return redirect('resumenEmpresa')
        else:
            print("entrando else")
            empresa2 = Empresa(nombre=request.POST["nombre"], nombreContribuyente=request.POST["contribuyente"], nit=request.POST["nit"], nrc=request.POST["nrc"], giro=request.POST["giro"])
            empresa2.save()
            print('save')
            return redirect('resumenEmpresa')

    return render(request, 'empresa/empresa.html', data)
