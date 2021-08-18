from django.db import models

# Create your models here.
from accounts.models import User, Profile 
from commons.models import Specialty

# Create your models here.
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain_prefix = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    class Meta: 
        abstract = True


class Staff(models.Model):

    class Meta: 
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    doctors = models.ManyToManyField(User, related_name='staff', blank=True, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE) 
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    
    def doctors_count(self):
        return self.doctors.count()

    
    def __str__(self):
        return f"{self.tenant.name}: {self.specialty.name}"
    
class TenantSettings(models.Model):
    color = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='tenant_logos', blank=True, null=True)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
