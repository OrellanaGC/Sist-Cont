from django.db import models
from apps.modulo.models import Modulo

# Create your models here.
class Permiso(models.Model):
    idPermiso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    modulo = models.ManyToManyField(Modulo)