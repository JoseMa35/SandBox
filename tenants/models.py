from django.db import models
from multiselectfield import MultiSelectField
from accounts.models import User, Profile
from commons.models import Specialty
from . import StatusQoutes


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
    address = models.CharField(
        max_length=500,
        blank=True,
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
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        related_name='bookings'
    )
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
    status = models.IntegerField(
        choices=StatusQoutes.choices,
        default=StatusQoutes.NEW
    )

    datetime = models.DateTimeField(
        auto_now=False,
        auto_now_add=False
    )
    meeting_link = models.CharField(
        max_length=100,
        blank=True, null=True
    )
    event_id = models.CharField(
        max_length=255,
        blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Fecha de registro
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return str(self.doctor_id)


class BookingDetail(models.Model):
    # booking 
    booking_id = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        null=True,
        related_name='booking_detail' 
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
    extra_info = models.TextField(
        # max_length=100,
        blank=True, null=True
    )
    brief_description = models.TextField(
        # max_length=100,
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
    
    def filename(self):
        return self.file.name.split('/')[-1]

class BookingDoctorDetail(models.Model):
    booking_detail = models.OneToOneField(
        BookingDetail,
        on_delete=models.CASCADE,
        related_name='doctor_detail'
    )
    description = models.TextField()


class BookingDoctorDetailFile(models.Model):
    booking_doctor_detail = models.ForeignKey(
        BookingDoctorDetail,
        on_delete=models.CASCADE,
        related_name='files_doctor'
    )
    file = models.FileField(
        upload_to='booking_attachments/'
    )

    def filename(self):
        return self.file.name.split('/')[-1]


class Staff(models.Model):
    doctors = models.ManyToManyField(
        User,
        # Profile,
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


    # def staffs_by_user(self, user_id):
    #     return Staff.objects.filter(doctors=user_id)


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
