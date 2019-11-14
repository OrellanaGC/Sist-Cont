from django.shortcuts import render, redirect
from apps.usuario.models import Usuario, Permiso
from django.contrib.auth import authenticate
import re

# Create your views here.
def resumenUsuarios(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios': usuarios}
    return render(request, 'usuario/usuarios.html', data)

def crearUsuario(request):
    permisos = Permiso.objects.all()
    data = {'permisos': permisos}
    if request.method == 'POST':
        errores = validarUsuario(request.POST['nombre'], request.POST['email'],
        request.POST['password'], request.POST['password2'])
        if len(errores) == 0:
            if not Usuario.objects.filter(email = request.POST['email']).exists():
                permiso = Permiso.objects.get(idPermiso=request.POST['permiso'])
                usuario = Usuario(nombre = request.POST['nombre'], email = request.POST['email'], permiso = permiso)
                usuario.set_password(request.POST['password'])
                usuario.save()
                return redirect('resumenUsuarios')
            else:
                printr("Usuario ya registrado")
        else:
            data = {'errores' : errores, 'permisos': permisos}
    return render(request, 'usuario/usuario.html', data)
def resumenUsuarios(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios': usuarios}
    return render(request, 'usuario/usuarios.html', data)
def actualizarMiUsuario(request):
    data = {}
    if request.method == 'POST':
        errores = validarUsuario(request.POST['nombre'], request.POST['email'], request.POST['password'])
        if not Usuario.objects.filter(email = request.POST['email']).exists():
            if len(errores) == 0:
                usuario = Usuario.objects.get(id=request.session['id'])
                usuario.nombre = request.POST['nombre']
                usuario.email = request.POST['email']
                usuario.set_password(request.POST['password'])
                usuario.save()
                request.session['nombre'] = request.POST['nombre']
                request.session['email'] = request.POST['email']
            else:
                data = {'errores' : errores}
        else:
            printr("Usuario ya registrado")
    return render(request, 'usuario/miUsuario.html', data)
def eliminarUsuario(request, idUsuario):
    usuario = Usuario.objects.get(id=idUsuario)
    usuario.delete()
    return redirect('resumenUsuarios')

def validarUsuario(nombre, email, password, password2):
    errores = set()
    if(len(password) < 6):
        errores.add('La contraseña debe tener al menos 6 caractéres')
    if not (password == password2):
        errores.add('Contraseñas diferentes')
    if(not re.match("^(([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)(\s*;\s*|\s*$))$", email)):
        errores.add('Email inválido')
    if(not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$", nombre)):
        errores.add('Nombre inválido')
    return errores
