# Generated by Django 2.2.5 on 2019-10-15 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marca', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='marca',
            name='estado',
            field=models.CharField(choices=[('A', 'ACTIVA'), ('D', 'DESHABILITADA')], default='A', max_length=1),
        ),
    ]
