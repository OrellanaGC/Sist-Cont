from django.db import models
from apps.producto.models import Producto

# Create your models here.
class Kardex(models.Model):
    idKardex = models.AutoField(primary_key=True)    
    stockMinimo= models.IntegerField()
    stockMaximo= models.IntegerField()    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    

class  Periodo(models.Model):
    idPeriodo =models.AutoField(primary_key=True)
    fechaInicio = models.DateField(auto_now=False)
    fechaFinal= models.DateField(auto_now=False, null=True, blank=True)    
    existenciaFinal= models.IntegerField()
    saldoFinal = models.FloatField()
    kardex= models.ForeignKey(Kardex, on_delete=models.CASCADE)

class LineaPeriodo(models.Model):
    idLineaPeriodo = models.AutoField(primary_key=True)
    factura = models.CharField(max_length=20)
    fecha= models.DateField(auto_now=False)
    tipoTransaccion = models.CharField(max_length=3)
    cantidadSobrante= models.IntegerField()
    costoUnitario= models.FloatField()
    cantidadEntrada = models.IntegerField()
    valorEntrada = models.FloatField()
    cantidadSalida = models.IntegerField()
    valorSalida = models.FloatField()
    cantidadExistencia = models.IntegerField()
    valorExistencia = models.FloatField()
    comprobacion = models.FloatField()
    periodo= models.ForeignKey(Periodo, on_delete=models.CASCADE)


    
          
    
   