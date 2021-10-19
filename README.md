```shell
<<<<<<< HEAD
python manage.py loaddata specialties.json gender.json document_type.json tenant.json tenant_settings.json user.json integration.json
```

```shell
python manage.py createsuperuser --email yahyr@gmail.com 
=======

python manage.py migrate --settings=core.settings.local
python manage.py loaddata specialties.json gender.json document_type.json tenant.json tenant_settings.json user.json integration.json --settings=core.settings.local
python manage.py createsuperuser --email yahyr@gmail.com --settings core.settings.local
>>>>>>> 0c9baca512853b4f1fd64c0bc2885c53d282b3b0
django-admin makemessages -l es
```

# How to run?

<<<<<<< HEAD
```shell
python3 manage.py runserver --settings core.settings.local
=======
```python
python manage.py runserver --settings core.settings.local
>>>>>>> 0c9baca512853b4f1fd64c0bc2885c53d282b3b0
```

Usuarios de prueba

yahyr@gmail.com
123456


USUARIO
Carlos Zavala
carlos@gmail.com
Lima123456

