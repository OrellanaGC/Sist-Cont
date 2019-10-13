from django.db import models

# Create your models here.
class TipoCuenta(models.Model):
    idTipoCuenta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    naturaleza = (
        ('D', 'DEBE'),
        ('H', 'HABER')
    )