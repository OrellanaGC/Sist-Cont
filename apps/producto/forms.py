from django import forms
from apps.producto.models import Producto


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

		]

		labels = {
		'nombre': 'Nombre',
		'descripcion':'Descripcion',
		#'existencias': 'Existencias',
		'marca': 'Marca',
		'categoria':'Categoria',
		'estado':'Estado',
		}

		widgets= {
		'nombre': forms.TextInput(attrs={'class':'form-control'}),
		'descripcion': forms.TextInput(attrs={'class':'form-control'}),
		'marca': forms.TextInput(attrs={'class':'form-control'}),
		'categoria': forms.TextInput(attrs={'class':'form-control'}),
		'estado': forms.Select(attrs={'class':'form-control'}),
		#'existencias': forms.TextInput(attrs={'class':'form-control'})		
		}

		def cleanNombre(self):
			nombre= self.cleaned_data.get('nombre')
			if nombre =="":
				raise forms.ValidationError("Ingresar el nombre del producto")
			return nombre;
		def cleanCategoria(self):
			categoria= self.cleaned_data.get('categoria')
			if categoria =="":
				raise forms.ValidationError("Ingresar la categoria del producto")
			return categoria;
		def cleanMarca(self):
			marca= self.cleaned_data.get('marca')
			if marca =="":
				raise forms.ValidationError("Ingresar la marca del producto")
			return marca;
		def cleanNombre(self):
			estado= self.cleaned_data.get('estado')
			if estado =="":
				raise forms.ValidationError("Ingresar el estado del producto")
			return estado;
		"""ef cleanExistencias(self):
			existencias= self.cleaned_data.get('existencias')
			if existencias >0 or existencias<0:
				raise forms.ValidationError("El producto debe inicializarse en 0 existencias")
			return existencias;"""