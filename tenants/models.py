from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.
from accounts.models import User, Profile
from commons.models import Specialty


# Create your models here.
class Tenant(models.Model):
    name = models.CharField(
        max_length=100
    )
    subdomain_prefix = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class Schedule(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedule'
    )


class ScheduleTimeFrame(models.Model):
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='time_frames'
    )
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    start_time = models.TimeField(
        auto_now=False,
        auto_now_add=False
    )
    end_time = models.TimeField(
        auto_now=False,
        auto_now_add=False
    )
    available = models.BooleanField(
        default=True
    )


class Booking(models.Model):
    doctor_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    client_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        blank=True, null=True
    )
    virtual_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=100
    )
    datetime = models.DateTimeField(
        auto_now=False,
        auto_now_add=False
    )
    meeting_link = models.CharField(
        max_length=100
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class BookingDetail(models.Model):
    booking_id = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        null=True
    )
    has_disability = models.BooleanField(
        default=False
    )
    smoke = models.BooleanField(
        default=False
    )
    drink = models.BooleanField(
        default=False
    )
    allergic = models.BooleanField(
        default=False
    )
    extra_info = models.CharField(
        max_length=100,
        blank=True, null=True
    )
    brief_description = models.TextField(
        max_length=100,
        blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class BookingDetailFile(models.Model):
    booking_detail = models.ForeignKey(
        BookingDetail,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(
        upload_to='booking_attachments/'
    )


class Staff(models.Model):
    doctors = models.ManyToManyField(
        User,
        related_name='staff',
        blank=True
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name='staff'
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='staff'
    )

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def doctors_count(self):
        return self.doctors.count()

    def __str__(self):
        return f"{self.tenant.name}: {self.specialty.name}"


class TenantSettings(models.Model):
    WEELDAYS = (
        ("Lunes", "Lunes"),
        ("Martes", "Martes"),
        ("Miercoles", "Miercoles"),
        ("jueves", "jueves"),
        ("Viernes", "Viernes"),
        ("Sabado", "Sabado"),
        ("Domingo", "Domingo"),
    )
    color = models.CharField(
        max_length=100
    )
    logo = models.ImageField(
        upload_to='core/static/images/tenants/',
        blank=True,
        null=True
    )
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    labor_days = MultiSelectField(
        choices=WEELDAYS
    )
    quote_duration = models.IntegerField(
        default=0,
    )
    wait_time = models.IntegerField(
        default=0,
    )
    work_start = models.DateTimeField()
    work_end = models.DateTimeField()
