from django.shortcuts import render
from apps.empresa.models import Empresa

# Create your views here.
def resumenEmpresa(request):
    empresa = Empresa.objects.first()
    data = {'empresa' : empresa}
    return render(request, 'empresa/empresa.html', data)

def guardarDatos(request):
    if Empresa.objects.count() > 0:
        if request.method == 'POST':
            empresa = Empresa.objects.first()
            empresa.nombre = request.POST["nombre"]
            empresa.nombreContribuyente = request.POST["contribuyente"]
            empresa.nit = request.POST["nit"]
            empresa.nrc = request.POST["nrc"]
            empresa.giro = request.POST["giro"]
            empresa.save()
    else:
        empresa = Empresa(nombre=request.POST["nombre"], nombreContribuyente=request.POST["contribuyente"], nit=request.POST["nit"], nrc=request.POST["nrc"], giro=request.POST["giro"])
        empresa.save()
    return render(request, 'empresa/empresa.html', data)