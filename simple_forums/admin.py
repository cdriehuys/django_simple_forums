from django.contrib import admin

from adminsortable.admin import SortableAdmin

from simple_forums import models

###########
# Inlines #
###########


class MessageInline(admin.StackedInline):
    """ Inline admin for Message model """

    model = models.Message
    fields = ('user', 'body',)
    extra = 1
    classes = ('collapse',)


################
# Model Admins #
################


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
            'fields': ('topic', 'title', 'sticky'),
        }),
        ('Date & Time Options', {
            'classes': ('collapse',),
            'fields': ('time_created',),
        }),
    )
    inlines = (MessageInline,)


class TopicAdmin(SortableAdmin):
    """ Admin for the topic model """

    fields = ('title', 'description',)


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Thread, ThreadAdmin)
admin.site.register(models.Topic, TopicAdmin)
