# Generated by Django 3.2.5 on 2021-10-06 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0004_alter_booking_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetail',
            name='brief_description',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bookingdetail',
            name='extra_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
