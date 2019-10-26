from django.shortcuts import render
from django.views.generic.list import ListView
#from django.views.generic import TemplateView
from apps.kardex.models import Kardex

def inventario(request):
    return render(request, 'inventario/inventario.html')

class ListaKardex(ListView):
	model= Kardex
	template_name='inventario/inventario.html'
	
	#def ListaInventario(self):
'''class ListarProductos(ListView):
	model= Producto
	template_name='inventario/inventario.html
class ListaKardex(ListView):
	template_name='inventario/inventario.html'
	context_object_name = 'kardex_list'
	queryset = Producto.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(ListaKardex, self).get_context_data(**kwargs)
		context['kardex'] = Kardex.objects.all()
		context['productos'] = self.queryset
		return context'''