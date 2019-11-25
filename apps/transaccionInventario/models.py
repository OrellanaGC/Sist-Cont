from django.db import models
from apps.kardex.models import Kardex
from apps.producto.models import Producto

# Create your models here.
class TransaccionInventario(models.Model):
    idTransaccionInv = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now=False)
    cantidadTransaccion = models.IntegerField()    
    valorUnitario = models.FloatField()    
    factura = models.CharField(max_length=20)
    TIPO = (
        ('I', 'INVENTARIO INICIAL'),
        ('C', 'COMPRA'),
        ('V', 'VENTA'),
        ('DC', 'DEVOLUCION DE COMPRA'),
        ('DV', 'DEVOLUCION DE VENTA')
    )
    tipo = models.CharField(max_length=2, choices=TIPO, default='I')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

