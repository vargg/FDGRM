from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

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
        'first_name',
        'email',
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    list_display_links = (
        'user',
    )
    search_fields = (
        'user',
        'author',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
