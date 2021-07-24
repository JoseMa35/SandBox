from django.contrib import admin

# Register your models here.
from specialties.models import Specialty_Doctor
from specialties.models import Specialty


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'position', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('position',)


@admin.register(Specialty_Doctor)
class SpecialtyDoctorAdmin(admin.ModelAdmin):
    list_display = ('_user', 'specialty', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('specialty',)
    ordering = ('specialty',)

    def _user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
