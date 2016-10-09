from django.contrib import admin
from django.db.models import Count

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
    date_hierarchy = 'time_created'
    fieldsets = (
        (None, {
            'fields': ('user', 'thread', 'body'),
        }),
        ('Date & Time Options', {
            'classes': ('collapse',),
            'fields': ('time_created',),
        }),
    )
    list_display = ('thread', 'user', 'time_created')
    search_fields = ('body', 'thread__title', 'user__username')


class ThreadAdmin(admin.ModelAdmin):
    """ Admin for the Thread model """
    date_hierarchy = 'time_last_activity'
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
    list_display = (
        'title', 'topic', 'show_replies', 'sticky', 'time_last_activity'
    )
    list_filter = ('sticky',)
    search_fields = ('title',)

    def show_replies(self, instance):
        return instance.replies
    show_replies.admin_order_field = 'replies'
    show_replies.short_description = 'replies'

    def get_queryset(self, request):
        """Return all thread instances"""
        return models.Thread.objects.annotate(replies=Count('message'))


class TopicAdmin(SortableAdmin):
    """ Admin for the topic model """
    fields = ('title', 'description',)
    list_display = ('title', 'show_thread_count')
    search_fields = ('title',)

    def get_queryset(self, request):
        """Include the number of threads in each topic."""
        return models.Topic.objects.annotate(thread_count=Count('thread'))

    def show_thread_count(self, instance):
        return instance.thread_count
    show_thread_count.admin_order_field = 'thread_count'
    show_thread_count.short_description = 'threads'


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Thread, ThreadAdmin)
admin.site.register(models.Topic, TopicAdmin)
