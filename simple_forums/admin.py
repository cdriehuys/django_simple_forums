from django.contrib import admin

from simple_forums import models


class MessageAdmin(admin.ModelAdmin):
    """ Admin for the Message model """

    class Meta:
        model = models.Message
        fields = ('user',)


class ThreadAdmin(admin.ModelAdmin):
    """ Admin for the Thread model """

    class Meta:
        model = models.Thread
        fields = ('title',)


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Thread, ThreadAdmin)
