# Generated by Django 3.2.5 on 2021-08-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('specialties', '0002_specialty_doctors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='doctors',
            field=models.ManyToManyField(blank=True, related_name='specialties', to='accounts.Profile'),
        ),
    ]
