# Generated by Django 3.2.5 on 2021-10-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0005_auto_20211006_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='meeting_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
