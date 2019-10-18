from django.shortcuts import render

# Create your views here.
def resumenUsuarios(request):
    return render(request, 'usuario/usuarios.html')
def crearUsuario(request):
    return render(request, 'usuario/usuario.html')
def actualizarMiUsuario(request):
    return render(request, 'usuario/miUsuario.html')
