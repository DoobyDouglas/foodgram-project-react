from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = (
        'username',
    )


admin.site.register(User, UserAdmin)
