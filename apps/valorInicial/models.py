from django.db import models
from apps.cuenta.models import Cuenta

# Create your models here.
class valorInicial(models.Model):
    idValor = models.AutoField(primary_key = True)
    fechaInicio = models.DateField(auto_now=False)
    fechaFinal = models.DateField(auto_now=False)
    ESTADOCUENTA = (
        ('A', 'ACREEEDORA'),
        ('D', 'DEUDORA'),
        ('S', 'SALDADA'),
        ('P', 'PATRIMONIO')
    )
    saldo = models.FloatField(null=True)
    estadoCuenta = models.CharField(max_length=1, choices=ESTADOCUENTA, default='S')
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)