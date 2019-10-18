from django.shortcuts import render

# Create your views here.
def resumenPermiso(request):
    return render(request, 'permiso/permiso.html')
