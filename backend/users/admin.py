from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_display_links = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )


admin.site.register(User, UserAdmin)
