# Generated by Django 3.2.5 on 2021-10-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0005_auto_20211006_0131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'verbose_name': 'Reserva', 'verbose_name_plural': 'Reservas'},
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(choices=[(0, 'Nueva'), (1, 'Confirmada'), (2, 'Sin Confirmar'), (3, 'Cancelada'), (4, 'No se presentó'), (5, 'Reagendada')], default=0),
        ),
    ]
