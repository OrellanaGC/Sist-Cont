from django.db import models
from apps.cuenta.models import Cuenta

# Create your models here.
class valorInicial(models.Model):
    idValor = models.AutoField(primary_key = True)
    fechaInicio = models.DateField(auto_now=False)
    fechaFinal = models.DateField(auto_now=False)
    estadoCuenta = (
        ('A', 'Acrededora'),
        ('D', 'Deudora'),
        ('P', 'Patrimonio')
    )
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)