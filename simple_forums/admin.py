from django.contrib import admin

from simple_forums import models


class MessageAdmin(admin.ModelAdmin):
    """ Admin for the Message model """

    fieldsets = (
        (None, {
            'fields': ('user', 'thread', 'body'),
        }),
        ('Date & Time Options', {
            'classes': ('collapse',),
            'fields': ('time_created',),
        }),
    )


class ThreadAdmin(admin.ModelAdmin):
    """ Admin for the Thread model """

    fields = ('title',)


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Thread, ThreadAdmin)
