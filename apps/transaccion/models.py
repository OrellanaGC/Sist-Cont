from django.db import models
from apps.cuenta.models import Cuenta

# Create your models here.
class Transaccion(models.Model):
    idTransaccion = models.AutoField(primary_key = True)
    detalle = models.CharField(max_length=250)
    monto = models.FloatField()
    fecha = models.DateField(auto_now=False)
    tipo = (
        ('C', 'CARGAR'),
        ('A', 'ABONAR')
    )
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)