# Generated by Django 3.2.5 on 2021-10-19 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0010_alter_staff_doctors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetail',
            name='booking_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_detail', to='tenants.booking'),
        ),
    ]
