# Generated by Django 2.2.5 on 2019-10-15 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoriaProducto', '0001_initial'),
        ('marca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
                ('existencias', models.IntegerField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categoriaProducto.CategoriaProducto')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marca.Marca')),
            ],
        ),
    ]