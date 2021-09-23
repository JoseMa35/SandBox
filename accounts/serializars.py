from rest_framework import serializers

from accounts.models import User, Profile
from commons.serializers import GenderSerializer, DocumentTypeSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    gender = GenderSerializer()
    document_type = DocumentTypeSerializer()

    class Meta:
        model = Profile
        fields = (
            'full_name',
            'gender',
            'document_type',
            'document',
            'cell_phone',
            'address',
            'date_of_birth',
            'user',)
