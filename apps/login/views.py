from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login as dj_login

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        usuario = authenticate(request, email=email, password=password)
        if usuario is not None:
            dj_login(request, usuario)
            user  = Usuario.objects.get(email=email)
            request.session['id'] = user.id
            request.session['nombre'] = user.nombre
            request.session['email'] = user.email
            request.session['permiso'] = user.permiso_id
            return redirect('/index/')
        else:
            return redirect('login')
    if 'id' in request.session:
        return redirect('/index/')
    return render(request, 'login/login.html')

def logout(request):
    del request.session['id']
    del request.session['nombre']
    del request.session['email']
    logout(request)
    return redirect(login)