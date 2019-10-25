from django.shortcuts import render
from django.views.generic.list import ListView
from apps.kardex.models import Kardex

def inventario(request):
    return render(request, 'inventario/inventario.html')

class ListaKardex(ListView):
	model= Kardex
	template_name='inventario/inventario.html'
	
	#def ListaInventario(self):
