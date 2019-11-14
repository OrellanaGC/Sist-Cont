from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as dj_login
from apps.usuario.models import Usuario
from apps.permiso.models import Permiso

# Create your views here.
def login(request):
    errores = set()
    data = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        usuario = authenticate(request, email=email, password=password)
        if usuario is not None:
            dj_login(request, usuario)
            user  = Usuario.objects.get(email=email)
            permiso = Permiso.objects.get(idPermiso=user.permiso_id)
            modulos = set()
            for modulo in permiso.modulo.all():
                modulos.add(modulo.nombre)
            request.session['id'] = user.id
            request.session['nombre'] = user.nombre
            request.session['email'] = user.email
            request.session['permiso'] = user.permiso_id
            request.session['modulos'] = list(modulos)
            return redirect('/index/')
        else:
            errores.add('Usuario no encontrado')
            data = {'errores' : errores}
            return render(request, 'login/login.html', data)
    if 'id' in request.session:
        return redirect('/index/')
    return render(request, 'login/login.html', data)

def logoutView(request):
    if request.session.get('id'):
        del request.session['id']
    if request.session.get('nombre'):
        del request.session['nombre']
    if request.session.get('email'):        
        del request.session['email']
    if request.session.get('permiso'):
        del request.session['permiso']
    if request.session.get('modulos'):
        del request.session['modulos']
    logout(request)
    return redirect(login)