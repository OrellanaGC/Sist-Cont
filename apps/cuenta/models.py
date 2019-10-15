from django.db import models

# Create your models here.
class Cuenta(models.Model):
    idCuenta = models.AutoField(primary_key=True)
    codigoCuenta = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    saldo = models.FloatField()
    cuentaPadre = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    modificaInventario = models.BooleanField()
    estadoCuenta = [
        ('A', 'ACREDEDORA'),
        ('D', 'DEUDORA'),
        ('S', 'SALDADA')
    ]
    tipo = [
        ('D', 'DEBE'),
        ('H', 'HABER')
    ]
    #nivel = models.IntegerField()
    estado = [
        ('A', 'ACTIVA'),
        ('D', 'DESHABILITADA')
    ]