# Generated by Django 3.2.5 on 2021-09-04 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0002_auto_20210904_2008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='integration',
            old_name='redirct',
            new_name='redirect',
        ),
    ]