from django.contrib import admin

from simple_forums import models


class ThreadAdmin(admin.ModelAdmin):
    """ Admin for the Thread model """

    class Meta:
        model = models.Thread
        fields = ('title',)


admin.site.register(models.Thread, ThreadAdmin)
