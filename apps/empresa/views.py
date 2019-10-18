from django.shortcuts import render

# Create your views here.
def resumenEmpresa(request):
    return render(request, 'empresa/empresa.html')
