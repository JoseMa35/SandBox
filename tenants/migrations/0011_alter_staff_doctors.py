# Generated by Django 3.2.5 on 2021-10-19 00:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenants', '0010_merge_0007_alter_staff_doctors_0009_booking_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='doctors',
            field=models.ManyToManyField(blank=True, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
    ]
