# Generated by Django 2.2.5 on 2019-10-15 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modulo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('idPermiso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('modulo', models.ManyToManyField(to='modulo.Modulo')),
            ],
        ),
    ]
