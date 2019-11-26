from django import forms
from apps.producto.models import Producto
from apps.transaccionInventario.models import *
from django.contrib.admin.widgets import AdminDateWidget

errores = {
    'required': 'Este campo es obligatorio',
    'invalid': 'El dato ingresado no es valido'
}


class ProductoForm(forms.ModelForm):

	class Meta:
		model = Producto
		fields =[
		'nombre',
		'descripcion',
		#'existencias',
		'marca',
		'categoria',
		'estado',
		'stockMinimo',
		'stockMaximo',

		]

		labels = {
		'nombre': 'Nombre',
		'descripcion':'Descripcion',
		#'existencias': 'Existencias',
		'marca': 'Marca',
		'categoria':'Categoria',
		'estado':'Estado',
		'stockMinimo':'Stock Minimo',
		'stockMaximo':'Stock Maximo',
		}

		widgets= {
		'nombre': forms.TextInput(attrs={'class':'form-control'}),
		'descripcion': forms.TextInput(attrs={'class':'form-control'}),
		'marca': forms.TextInput(attrs={'class':'form-control'}),
		'categoria': forms.Select(attrs={'class':'form-control'}),
		'estado': forms.Select(attrs={'class':'form-control'}),
		'stockMinimo': forms.TextInput(attrs={'class':'form-control'}),
		'stockMaximo': forms.TextInput(attrs={'class':'form-control'})
		#'existencias': forms.TextInput(attrs={'class':'form-control'})		
		}

		def cleanNombre(self):
			nombre= self.cleaned_data.get('nombre')
			if nombre =="":
				raise forms.ValidationError("Ingresar el nombre del producto")
			return nombre
		def cleanCategoria(self):
			categoria= self.cleaned_data.get('categoria')
			if categoria =="":
				raise forms.ValidationError("Ingresar la categoria del producto")
			return categoria
		def cleanMarca(self):
			marca= self.cleaned_data.get('marca')
			if marca =="":
				raise forms.ValidationError("Ingresar la marca del producto")
			return marca
		def cleanNombre(self):
			estado= self.cleaned_data.get('estado')
			if estado =="":
				raise forms.ValidationError("Ingresar el estado del producto")
			return estado
		def cleanStockMinimo(self):
			stockMinimo= self.cleaned_data.get('stockMinimo')
			if stockMinimo <0:
				raise forms.ValidationError("No puede haber stock negativo")
			return stockMinimo
		def cleanStockMaximo(self):
			stockMaximo= self.cleaned_data.get('stockMaximo')
			if stockMaximo <self.stockMinimo:
				raise forms.ValidationError("stock maximo debe ser mayor que stock minimo")
			return stockMaximo
		"""ef cleanExistencias(self):
			existencias= self.cleaned_data.get('existencias')
			if existencias >0 or existencias<0:
				raise forms.ValidationError("El producto debe inicializarse en 0 existencias")
			return existencias;"""


class DateInput(forms.DateInput):
	input_type='date'

class transInvForm(forms.ModelForm):

	class Meta:
		model = TransaccionInventario
		fields =[
		'fecha',
		'cantidadTransaccion',
		#'existencias',
		'valorUnitario',
		'factura',		
		'tipo',
		'producto',

		]

		labels = {
		'fecha': 'Fecha',
		'cantidadTransaccion':'cantidad',
		#'existencias': 'Existencias',
		'valorUnitario': 'valor Unitario',
		'factura':'Factura',
		'tipo':'tipo',
		'producto':'Producto',
		
		}

		widgets= {
		'fecha': DateInput(attrs={'class':'form-control'}),
		'cantidadTransaccion': forms.TextInput(attrs={'class':'form-control'}),
		'valorUnitario': forms.TextInput(attrs={'class':'form-control'}),
		'factura': forms.TextInput(attrs={'class':'form-control'}),
		'tipo': forms.Select(attrs={'class':'form-control'}),
		'producto': forms.Select(attrs={'class':'form-control'}),		
		}