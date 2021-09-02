from django.contrib import admin

# Register your models here.
from commons.models import Gender, Document_Type, Specialty, Integration, IntegrationKey


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name', 'is_active')


@admin.register(Document_Type)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('long_name', 'short_name', 'character_length', 'type_character', 'is_active')


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'position', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('position',)


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active',)


@admin.register(IntegrationKey)
class IntegrationKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'integration', 'token',)

    def _user(self):
        return self.user.email
