from django.db import models

# Create your models here.
class Cuenta(models.Model):
    idCuenta = models.AutoField(primary_key=True)
    codigoCuenta = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    saldo = models.FloatField()
    cuentaPadre = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    modificaInventario = models.BooleanField()
    ESTADOCUENTA = (
        ('A', 'ACREDEDORA'),
        ('D', 'DEUDORA'),
        ('S', 'SALDADA')
    )
    TIPO = (
        ('D', 'DEBE'),
        ('H', 'HABER')
    )    
    ESTADO = (
        ('A', 'ACTIVA'),
        ('D', 'DESHABILITADA')
    )
    estadoCuenta = models.CharField(max_length=1, choices=ESTADOCUENTA, default='S')
    tipo = models.CharField(max_length=1, choices=TIPO, default='D')
    estado = models.CharField(max_length=1, choices=ESTADO, default='A')