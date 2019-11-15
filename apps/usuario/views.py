from django.shortcuts import render, redirect
from apps.usuario.models import Usuario, Permiso
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import re

# Create your views here.
@login_required
def resumenUsuarios(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios': usuarios}
    return render(request, 'usuario/usuarios.html', data)

@login_required
def crearUsuario(request):
    permisos = Permiso.objects.all()
    data = {'permisos': permisos}
    errores = set()
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
                #printr("Usuario ya registrado")
                errores.add("Usuario ya registrado")
                data = {'usuario' : usuario, 'errores' : errores}
        else:
            data = {'errores' : errores, 'permisos': permisos}
    return render(request, 'usuario/usuario.html', data)

@login_required
def actualizarMiUsuarioResumen(request):
    usuario = Usuario.objects.get(id=request.session['id'])
    data = {'usuario' : usuario, 'editando': False}
    return render(request, 'usuario/miUsuario.html', data)


@login_required
def actualizarMiUsuario(request):
    data = {}
    usuario = Usuario.objects.get(id=request.session['id'])
    errores = set()
    data = {'usuario' : usuario, 'errores' : errores, 'editando': True}
    if request.method == 'POST':
        errores = validarUsuario(request.POST['nombre'], request.POST['email'], request.POST['password'], request.POST['password2'])
        if not Usuario.objects.filter(email = request.POST['email']).exists():
            if len(errores) == 0:
                #usuario = Usuario.objects.get(id=request.session['id'])
                usuario.nombre = request.POST['nombre']
                usuario.email = request.POST['email']
                usuario.set_password(request.POST['password'])
                usuario.save()
                request.session['nombre'] = request.POST['nombre']
                request.session['email'] = request.POST['email']
            else:
                data = {'usuario' : usuario, 'errores' : errores, 'editando':True}
        else:
            errores.add("Usuario ya registrado")
            data = {'usuario' : usuario, 'errores' : errores, 'editando':True}
    return render(request, 'usuario/miUsuario.html', data)

@login_required
def actualizarUsuario(request, idUsuario):
    data = {}
    permisos = Permiso.objects.all()
    usuario = Usuario.objects.get(id=idUsuario)
    errores = set()
    if request.method == 'POST':
        errores = validarUsuario(request.POST['nombre'], request.POST['email'], request.POST['password'], request.POST['password2'])
        if not (Usuario.objects.filter(email = request.POST['email']).exists()) or request.POST['email'] == usuario.email:
            if len(errores) == 0:
                usuario = Usuario.objects.get(id=idUsuario)
                usuario.nombre = request.POST['nombre']
                usuario.email = request.POST['email']
                usuario.permiso_id = request.POST['permiso']
                usuario.set_password(request.POST['password'])
                usuario.save()
                request.session['nombre'] = request.POST['nombre']
                request.session['email'] = request.POST['email']
                return redirect('resumenUsuarios')
            else:
                data = {'usuario' : usuario, 'errores' : errores, 'permisos': permisos}
                return render(request, 'usuario/usuario.html', data)
        else:
            errores.add("Usuario ya registrado")
            data = {'usuario' : usuario, 'errores' : errores, 'permisos': permisos}
            return render(request, 'usuario/usuario.html', data)
    data = {'errores' : errores, 'permisos' : permisos, 'usuario' : usuario}
    return render(request, 'usuario/usuario.html', data)

@login_required
def eliminarUsuario(request, idUsuario):
    usuario = Usuario.objects.get(id=idUsuario)
    usuario.delete()
    return redirect('resumenUsuarios')

def validarUsuario(nombre, email, password, password2):
    errores = set()
    if(len(password) < 6) and password:
        errores.add('La contraseña debe tener al menos 6 caractéres')
    if not (password == password2):
        errores.add('Contraseñas diferentes')
    if(not re.match("^(([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)(\s*;\s*|\s*$))$", email)):
        errores.add('Email inválido')
    if(not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ0-9 ]+$", nombre)):
        errores.add('Nombre inválido')
    return errores
