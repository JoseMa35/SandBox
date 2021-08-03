"""Commons serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import (Specialty, Specialty_Doctor)


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ('id', 'name', 'description', 'is_active')


class SpecialtyDoctorSerializer(serializers.ModelSerializer):
    specialty_id = serializers.IntegerField(source='specialty.id')
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    avatar = serializers.CharField(source='user.profile.avatar')
    specialty = serializers.CharField(source='specialty.name')
    full_name = serializers.CharField(source='user.profile.full_name')

    class Meta:
        model = Specialty_Doctor
        fields = (
            'id',
            # Specialty
            'specialty', 'specialty_id',
            # User
            'user_id', 'first_name', 'last_name', 'full_name',
            # Profile
            'avatar'
        )
