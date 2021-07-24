from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    # password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'father_last_name',
            'mother_last_name',
        )


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source='user.email',
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        source='user.password',
        required=False,
        max_length=128,
        write_only=True,
        validators=[validate_password]
    )
    first_name = serializers.CharField(source='user.first_name')
    father_last_name = serializers.CharField(source='user.father_last_name')
    mother_last_name = serializers.CharField(source='user.mother_last_name')
    is_active = serializers.BooleanField(source='user.is_active')

    class Meta:
        model = Profile
        fields = (
            # User
            'email', 'password', 'first_name',
            'father_last_name', 'mother_last_name', 'is_active',
            # Profile
            'user', '_gender',
            '_document_type', 'document', 'cell_phone', 'date_of_birth',)
