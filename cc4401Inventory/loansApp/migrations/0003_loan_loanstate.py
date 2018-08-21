# Generated by Django 2.0.5 on 2018-08-11 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loansApp', '0002_loan_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='loanState',
            field=models.CharField(choices=[('V', 'Vigente'), ('C', 'Caducado'), ('P', 'Perdido'), ('R', 'Recibido')], default='V', max_length=1, verbose_name='EstadoPrestamo'),
        ),
    ]
