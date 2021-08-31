from tenants.models import Schedule, ScheduleTimeFrame, Staff, Tenant, TenantSettings
from accounts.models import User, Profile, Appointment
from commons.serializers import SpecialtySerializer

from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id', 'specialty', 'doctors')


class TenantSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSettings
        fields = ('color', 'logo')


class TenantSerializer(serializers.ModelSerializer):
    settings = TenantSettingsSerializer(read_only=True)

    class Meta:
        model = Tenant
        fields = ('id', 'subdomain_prefix', 'name', 'settings')


class TenantStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True, many=True)

    class Meta:
        model = Tenant
        fields = ('id', 'subdomain_prefix', 'name', 'staff')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ('avatar', 'full_name', 'user')


class DoctorSerializer(serializers.ModelSerializer):
    profile = DoctorProfileSerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'profile', 'specialty')


class PatientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)


class PatientProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False, allow_blank=True, )
    gender = serializers.CharField(required=False)
    age = serializers.CharField(required=False)
    document_type = serializers.IntegerField(required=False)
    document = serializers.CharField(required=False)
    is_disability = serializers.BooleanField(required=False, default=False)
    is_smoker = serializers.BooleanField(required=False, default=False)
    is_alcohol = serializers.BooleanField(required=False, default=False)
    is_allegiance = serializers.BooleanField(required=False, default=False)
    allegiance_detail = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('full_name', 'gender', 'age', 'document_type',
                  'document', 'is_disability', 'is_smoker', 'is_alcohol',
                  'is_allegiance', 'allegiance_detail')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.document_type = validated_data.get('document_type', instance.document_type)
        instance.document = validated_data.get('document', instance.document)
        instance.is_disability = validated_data.get('is_disability', instance.is_disability)
        instance.is_smoker = validated_data.get('is_smoker', instance.is_smoker)
        instance.is_alcohol = validated_data.get('is_alcohol', instance.is_alcohol)
        instance.is_allegiance = validated_data.get('is_allegiance', instance.is_allegiance)
        instance.allegiance_detail = validated_data.get('allegiance_detail', instance.allegiance_detail)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Create and return a new `Appointment` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)


class PatientAppointmentSerializer(serializers.ModelSerializer):
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    specialty = serializers.IntegerField()
    doctor = serializers.IntegerField()
    profile = PatientProfileSerializer()

    class Meta:
        model = Appointment
        fields = ('description', 'specialty', 'doctor', 'profile')

    def create(self, validated_data):
        """
        Create and return a new `Appointment` instance, given the validated data.
        """
        return Appointment.objects.create(**validated_data)


class ScheduleTimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTimeFrame
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleTimeFrameSerializer(read_only=True, many=True)

    class Meta:
        model = Schedule
        fields = ('doctor', 'schedule')
