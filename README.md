```shell
python manage.py loaddata specialties.json gender.json document_type.json tenant.json tenant_settings.json user.json integration.json --settings=core.settings.local
python manage.py createsuperuser --email yahyr@gmail.com 
django-admin makemessages -l es
```

# How to run 

```python
python3 manage.py runserver --settings core.settings.local
```

Usuarios de prueba

yahyr@gmail.com
123456


USUARIO
Carlos Zavala
carlos@gmail.com
Lima123456

