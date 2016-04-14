from django.contrib import admin

from simple_forums.notifications import models


class ThreadNotificationAdmin(admin.ModelAdmin):
    """ Admin for the ThreadNotification model """

    fields = ('user', 'thread')


admin.site.register(models.ThreadNotification, ThreadNotificationAdmin)
