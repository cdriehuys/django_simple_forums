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

    fieldsets = (
        (None, {
            'fields': ('topic', 'title'),
        }),
        ('Date & Time Options', {
            'classes': ('collapse',),
            'fields': ('time_created',),
        }),
    )


class TopicAdmin(admin.ModelAdmin):
    """ Admin for the topic model """

    fields = ('title', 'description',)


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Thread, ThreadAdmin)
admin.site.register(models.Topic, TopicAdmin)
