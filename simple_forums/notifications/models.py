from django.conf import settings
from django.db import models


class ThreadNotification(models.Model):
    """ Class to handle notifications about threads """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    thread = models.ForeignKey('simple_forums.Thread')

    def __str__(self):
        """ Return a string representation of the instance """
        return 'Notify %s of changes to thread #%d (%s)' % (
            self.user.username, self.thread.id, self.thread)
