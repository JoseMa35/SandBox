# Generated by Django 3.2.5 on 2021-08-18 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0004_tenantsettingsmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TenantSettingsModel',
            new_name='TenantSettings',
        ),
    ]
