# Generated by Django 3.2.5 on 2021-10-14 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_email'),
        ('tenants', '0006_auto_20211013_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='doctors',
            field=models.ManyToManyField(blank=True, related_name='staff', to='accounts.Profile'),
        ),
    ]
