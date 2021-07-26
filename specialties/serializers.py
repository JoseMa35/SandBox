"""Commons serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import (Specialty, Specialty_Doctor)


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        # fields = '__all__'
        fields = ('id', 'name', 'description', 'is_active')


class SpecialtyDoctorSerializer(serializers.ModelSerializer):
    specialty_id = serializers.IntegerField(source='specialty.id')
    user_id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(source='user.name')
    father_lastname = serializers.CharField(source='user.father_lastname')
    mother_lastname = serializers.CharField(source='user.mother_lastname')
    avatar = serializers.CharField(source='user.profile.avatar')
    specialty = serializers.CharField(source='specialty.name')
    full_name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Specialty_Doctor
        # fields = '__all__'
        fields = (
            'id',
            # Specialty
            'specialty', 'specialty_id',
            # User
            'user_id', 'name', 'father_lastname', 'mother_lastname', 'full_name',
            # Profile
            'avatar'
        )
