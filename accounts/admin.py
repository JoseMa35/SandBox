from django.contrib import admin
from django.contrib.auth.forms import (UserCreationForm, )

from django.contrib.auth.admin import UserAdmin

from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

from .models import User, Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'gender', 'document_type', 'document', 'cell_phone',
        'is_doctor', 'is_patient', 'is_admin',
        'is_active', 'is_deleted', 'is_blocked',)
    list_filter = ('is_doctor', 'is_patient', 'is_admin', 'document_type')
    search_fields = ('user__email',)
    ordering = ('user__email',)
    readonly_fields = ('id',)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', ]


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1
    can_delete = False


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('email', 'password', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

