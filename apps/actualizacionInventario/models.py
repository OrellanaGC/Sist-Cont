from django.db import models
from apps.transaccionInventario.models import TransaccionInventario
from apps.kardex.models import Kardex

# Create your models here.
class ActualizacionInventario(models.Model):
    idActualzacion = models.AutoField(primary_key=True)
    existencias = models.IntegerField()
    costoUnitario = models.FloatField()
    costoTotal = models.FloatField()
    kardex = models.ForeignKey(Kardex, on_delete=models.CASCADE)
    transaccionInventario = models.ForeignKey(TransaccionInventario, on_delete=models.CASCADE)
