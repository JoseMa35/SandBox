# Generated by Django 3.2.5 on 2021-08-14 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specialties', '0003_auto_20210814_0808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='doctors',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='speciality',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='tenant',
        ),
        migrations.DeleteModel(
            name='Specialty',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
    ]