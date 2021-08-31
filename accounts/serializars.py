from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User, Profile, Appointment
from commons.models import Gender
from commons.serializers import GenderSerializer, DocumentTypeSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    gender = GenderSerializer()
    document_type = DocumentTypeSerializer()

    class Meta:
        model = Profile
        fields = ('gender', 'document_type', 'document', 'cell_phone', 'date_of_birth', 'user',)

