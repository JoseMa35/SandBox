# Generated by Django 3.2.5 on 2021-09-10 18:40

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0002_auto_20210909_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenantsettings',
            name='weekend',
        ),
        migrations.AddField(
            model_name='tenantsettings',
            name='labor_days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miercoles', 'Miercoles'), ('jueves', 'jueves'), ('Viernes', 'Viernes'), ('Sabado', 'Sabado'), ('Domingo', 'Domingo')], default=2, max_length=52),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tenantsettings',
            name='quote_duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tenantsettings',
            name='wait_time',
            field=models.IntegerField(default=0),
        ),
    ]