from django.shortcuts import render, redirect
from apps.permiso.models import Permiso
from apps.modulo.models import Modulo
# Create your views here.

def resumenPermiso(request):
    #permiso = Permiso.objects.get(idPermiso=request.session['id'])
    permisos = Permiso.objects.all()
    data = {'permisos' : permisos}
    if request.method == 'POST':
        nuevoPermiso = Permiso()
        nuevoPermiso.save()
        nuevoPermiso.nombre = request.POST["nombre"]
        if int(request.POST.get("producto", 0)) == 1:
            modulo1 = Modulo.objects.get(idModulo=1)
            nuevoPermiso.modulo.add(modulo1)
        if int(request.POST.get("kardex", 0)) == 2:
            modulo2 = Modulo.objects.get(idModulo=2)
            nuevoPermiso.modulo.add(modulo2)
        if int(request.POST.get("libroDiario", 0)) == 3:
            modulo3 = Modulo.objects.get(idModulo=3)
            nuevoPermiso.modulo.add(modulo3)
        if int(request.POST.get("cuenta", 0)) == 4:
            modulo4 = Modulo.objects.get(idModulo=4)
            nuevoPermiso.modulo.add(modulo4)
        if int(request.POST.get("categoriaProducto", 0)) == 5:
            modulo5 = Modulo.objects.get(idModulo=5)
            nuevoPermiso.modulo.add(modulo5)
        if int(request.POST.get("empresa", 0)) == 6:
            modulo6 = Modulo.objects.get(idModulo=6)
            nuevoPermiso.modulo.add(modulo6)
        nuevoPermiso.save()
        return redirect('resumenPermiso')
    return render(request, 'permiso/permiso.html', data)


def editarPermiso(request, idPermiso):
    permiso = Permiso.objects.get(idPermiso=idPermiso)
    modulos = Modulo.objects.all()
    data = {'permiso' : permiso, 'modulos' : modulos}
    if request.method == 'POST':
        p.nombre = request.POST["nombre"]
        modulosPermiso = request.POST.getlist('modulos[]')
        for modulo in modulosPermiso:
            modulo = Modulo.objects.get(idModulo=modulo)
            permiso.modulo.add(modulo)
        p.save()
    return render(request, 'permiso/permiso.html', data)

def eliminarPermiso(requesr, idPermiso):
    permiso = Permiso.objects.get(idPermiso=request.session['id'])
    permiso.delete()
    return redirect('resumenPermiso')
