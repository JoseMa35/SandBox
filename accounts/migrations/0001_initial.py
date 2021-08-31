# Generated by Django 3.2.5 on 2021-08-31 20:11

import accounts.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=150, null=True, verbose_name='username')),
                ('email', models.EmailField(help_text='Correo electrónico', max_length=254, unique=True, verbose_name='email')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('document', models.CharField(max_length=15, unique=True)),
                ('age', models.CharField(blank=True, max_length=50, null=True)),
                ('cell_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('about', models.TextField(blank=True, max_length=1000, null=True)),
                ('avatar', models.ImageField(default='core/static/images/avatar/default.jpeg', upload_to='core/static/images/avatar/')),
                ('is_disability', models.BooleanField(blank=True, default=False)),
                ('is_smoker', models.BooleanField(blank=True, default=False)),
                ('is_alcohol', models.BooleanField(blank=True, default=False)),
                ('is_allegiance', models.BooleanField(blank=True, default=False)),
                ('allegiance_detail', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_patient', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.document_type')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.gender')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='accounts.profile')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='commons.specialty')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointment',
            },
        ),
    ]
