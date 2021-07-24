"""Commons serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import (Gender, Document_Type)


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_Type
        fields = '__all__'



