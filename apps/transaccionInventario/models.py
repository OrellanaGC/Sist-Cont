from django.db import models
from apps.kardex.models import Kardex

# Create your models here.
class TransaccionInventario(models.Model):
    idTransaccionInv = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now=False)
    cantidad = models.IntegerField()
    costoUnitario = models.FloatField()
    costoTotal = models.FloatField()
    detalle = models.CharField(max_length=150)
    tipo = (
        ('I', 'INVENTARIO INICIAL'),
        ('C', 'COMPRA'),
        ('V', 'VENTA'),
        ('DC', 'DEVOLUCION DE COMPRA'),
        ('DV', 'DEVOLUCION DE VENTA')
    )
    kardex = models.ForeignKey(Kardex, on_delete=models.CASCADE)