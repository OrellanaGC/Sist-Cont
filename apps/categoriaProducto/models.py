from django.db import models

# Create your models here.
class CategoriaProducto(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=50)
    estado = (
        ('A', 'ACTIVA'),
        ('D', 'DESHABILITADA')
    )