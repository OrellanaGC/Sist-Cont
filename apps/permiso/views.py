from django.shortcuts import render
from apps.permiso.models import Permiso
from apps.modulo.models import Modulo
# Create your views here.

def resumenPermiso(request):
    #permiso = Permiso.objects.get(idPermiso=request.session['id'])
    permisos = Permiso.objects.all()
    data = {'permisos' : permisos}
    return render(request, 'permiso/permiso.html')

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