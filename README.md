```shell
python manage.py migrate --settings=core.settings.local
python manage.py loaddata specialties.json gender.json document_type.json tenant.json tenant_settings.json user.json integration.json --settings=core.settings.local
python manage.py createsuperuser --email yahyr@gmail.com --settings core.settings.local
```

# How to run?

```shell
python3 manage.py runserver --settings core.settings.local
```

Usuarios de prueba

yahyr@gmail.com
123456


USUARIO
Carlos Zavala
carlos@gmail.com
Lima123456

