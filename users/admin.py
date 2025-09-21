from django.contrib import admin

from users.models import Notification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
