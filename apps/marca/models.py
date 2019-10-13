from django.db import models

# Create your models here.
class Marca(models.Model):
    idMarca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    estado = (
        ('A', 'ACTIVA'),
        ('D', 'DESHABILITADA')
    )