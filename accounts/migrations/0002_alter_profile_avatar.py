# Generated by Django 3.2.5 on 2021-07-24 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='static/images/avatar/default.jpg', upload_to='static/images/avatar/'),
        ),
    ]
