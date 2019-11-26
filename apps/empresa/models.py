from django.db import models

# Create your models here.
class Empresa(models.Model):
    idEmpresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nombreContribuyente = models.CharField(max_length=50)
    nit = models.CharField(max_length=17)
    nrc = models.CharField(max_length=10)
    giro = models.CharField(max_length=30)
