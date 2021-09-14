from django.db.models.base import Model
from tenants.models import (
    Schedule,
    ScheduleTimeFrame,
    Staff,
    Tenant,
    TenantSettings,
    Booking,
    BookingDetail,
    BookingDetailFile
)
from accounts.models import User, Profile
from commons.serializers import SpecialtySerializer

from rest_framework import fields, serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id', 'specialty', 'doctors')


class TenantSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSettings
        fields = [
            'color',
            'logo',
            'labor_days',
            'quote_duration',
            'wait_time',
            'work_start',
            'work_end',
        ]


class TenantSerializer(serializers.ModelSerializer):
    settings = TenantSettingsSerializer(read_only=True)

    class Meta:
        model = Tenant
        fields = ('id', 'subdomain_prefix', 'name', 'settings', 'description')


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


class ScheduleTimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTimeFrame
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleTimeFrameSerializer(read_only=True, many=True)

    class Meta:
        model = Schedule
        fields = ('doctor', 'schedule')


class BookingDetailFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDetailFile
        fields = ["file"]


class BookingDetailSerializer(serializers.ModelSerializer):
    files = BookingDetailFileSerializer(many=True)

    class Meta:
        model = BookingDetail
        fields = [
            # "booking_id"
            "has_disability",
            "smoke",
            "drink",
            "allergic",
            "extra_info",
            "brief_description",
            "created_at",
            "updated_at",
            "files"
        ]


class BookingSerializer(serializers.ModelSerializer):
    booking_detail = BookingDetailSerializer(source="bookingdetail")

    class Meta:
        model = Booking
        fields = [
            "doctor_id",
            "client_id",
            "virtual_profile",
            "status",
            "datetime",
            "meeting_link",
            "created_at",
            "updated_at",
            "booking_detail"
        ]

    def save(self):
        print(self.validated_data)
        booking_data = self.validated_data
        booking_detail_data = booking_data.pop('bookingdetail')

        booking = Booking.objects.create(**booking_data)
        BookingDetail.objects.create(booking_id=booking, **booking_detail_data)

        return booking
