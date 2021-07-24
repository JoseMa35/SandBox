from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, father_lastname, mother_lastname,
                     password, **extra_fields):
        if not email:
            raise ValueError('The Document must be set')
        user = self.model(email=email, name=name,
                          father_lastname=father_lastname, mother_lastname=mother_lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name=None, father_lastname=None, mother_lastname=None,
                    password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, name, father_lastname, mother_lastname,
                                 password, **extra_fields)

    def create_superuser(self, email, name=None, father_lastname=None, mother_lastname=None,
                         password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, father_lastname, mother_lastname,
                                 password, **extra_fields)
