# Generated by Django 2.2.5 on 2019-10-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0002_auto_20191015_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='estado',
            field=models.CharField(choices=[('A', 'ACTIVA'), ('D', 'DESHABILITADA')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='estadoCuenta',
            field=models.CharField(choices=[('A', 'ACREDEDORA'), ('D', 'DEUDORA'), ('S', 'SALDADA')], default='S', max_length=1),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='tipo',
            field=models.CharField(choices=[('D', 'DEBE'), ('H', 'HABER')], default='D', max_length=1),
        ),
    ]
