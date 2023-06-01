from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = (
        'username',
        'role',
    )


admin.site.register(User, UserAdmin)
