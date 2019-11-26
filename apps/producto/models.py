from django.db import models



# Create your models here.
class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    existencias = models.IntegerField(default=0)
    stockMinimo= models.IntegerField()
    stockMaximo= models.IntegerField() 
    #marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    #categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    marca= models.CharField(max_length=20)
    CATEGORIA = (
        ('Bolsos para Hombres', 'Bolsos para hombres'),
        ('Bolsos para Mujeres', 'Bolsos para mujeres')
    )
    categoria= models.CharField(max_length=20, choices=CATEGORIA, default='Bolsos para Mujeres')
    ESTADO = (
        ('Activo', 'ACTIVO'),
        ('Deshabilitado', 'DESHABILITADO')
    )
    estado = models.CharField(max_length=15, choices=ESTADO, default='')

    def __str__(self):
        return self.nombre
        


        