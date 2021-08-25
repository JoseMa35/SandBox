"""Commons serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import (Gender, Document_Type, Specialty)


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        # fields = '__all__'
        fields = ('short_name', 'long_name')


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_Type
        # fields = '__all__'
        fields = ('long_name', 'short_name', 'character_length', 'type_character')


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        # fields = '__all__'
        fields = ('id', 'name', 'description')
