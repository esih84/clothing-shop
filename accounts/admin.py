from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import *
from .models import *
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ('email', 'username')
    list_filter = ('email', 'is_active')
    fieldsets = (
        ('user', {'fields': ('email', 'password')}),
        ('personal info', {'fields': ('is_admin',)}),
        ('permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(profile)
admin.site.register(comment)