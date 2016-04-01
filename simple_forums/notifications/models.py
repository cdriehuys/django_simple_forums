from django.conf import settings
from django.core import mail
from django.db import models


class ThreadNotification(models.Model):
    """ Class to handle notifications about threads """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    thread = models.ForeignKey('simple_forums.Thread')

    def __str__(self):
        """ Return a string representation of the instance """
        return 'Notify %s of changes to thread #%d (%s)' % (
            self.user.username, self.thread.id, self.thread)

    def send_notification(self, message):
        """ Notify user that the given message has been posted """
        subject = 'Thread Updated'
        message = 'Thread #%d was updated' % self.thread.pk

        mail.send_mail(
            subject, message, 'no-reply@example.com',
            (self.user.email,))
