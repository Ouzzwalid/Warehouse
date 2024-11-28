from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from user.forms import CreateUserForm, UpdateUserForm

User = get_user_model()
class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = UpdateUserForm
    model = User
    list_display = ('username', 'email', 'role')
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email','phone')
        }), 
        ('Role', {
            'fields': ('role',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
       
    )

admin.site.register(User, CustomUserAdmin)
# Register your models here.
