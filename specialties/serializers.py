"""Commons serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import (Specialty, Specialty_Doctor)


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class SpecialtyDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty_Doctor
        fields = '__all__'

