# Generated by Django 2.2.5 on 2019-10-12 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('idCuenta', models.AutoField(primary_key=True, serialize=False)),
                ('codigoCuenta', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('saldo', models.FloatField()),
                ('modificaInventario', models.BooleanField()),
                ('cuentaPadre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuenta.Cuenta')),
            ],
        ),
    ]
