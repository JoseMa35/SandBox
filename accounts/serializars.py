from rest_framework import serializers

from accounts.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            # 'password',
        )


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'id',
            'full_name',
            'gender',
            'document_type',
            'document',
            'cell_phone',
            'address',
            'date_of_birth',
            # 'email',
            'user',
        )

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.document_type = validated_data.get('document_type', instance.document_type)
        instance.document = validated_data.get('document', instance.document)
        instance.cell_phone = validated_data.get('cell_phone', instance.cell_phone)
        instance.address = validated_data.get('address', instance.address)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance
