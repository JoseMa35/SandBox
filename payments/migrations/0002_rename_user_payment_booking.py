# Generated by Django 3.2.5 on 2021-10-18 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='user',
            new_name='booking',
        ),
    ]
