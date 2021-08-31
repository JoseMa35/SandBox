# Generated by Django 3.2.5 on 2021-08-25 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0002_specialty'),
        ('tenants', '0008_alter_staff_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='commons.specialty'),
        ),
    ]
