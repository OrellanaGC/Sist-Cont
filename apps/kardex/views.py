from django.shortcuts import render

def inventario(request):
    return render(request, 'inventario/inventario.html')