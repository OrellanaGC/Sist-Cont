from django.db import models
from apps.producto.models import Producto

# Create your models here.
class Kardex(models.Model):
    idKardex = models.AutoField(primary_key=True)
    fechaInicio = models.DateField(auto_now=False)
    fechaFin = models.DateField(auto_now=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)