from django.conf import settings
from django.core import mail
from django.db import models
from django.template.loader import get_template

try:
    from django.template.exceptions import TemplateDoesNotExist
except ImportError:
    from django.template.base import TemplateDoesNotExist


class ThreadNotification(models.Model):
    """ Class to handle notifications about threads """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    thread = models.ForeignKey('simple_forums.Thread')

    def __str__(self):
        """ Return a string representation of the instance """
        return 'Notify %s of changes to thread #%d (%s)' % (
            self.user.username, self.thread.id, self.thread)

    def _email_context(self):
        """ Get context used for sending emails """
        return {}

    @staticmethod
    def _full_template_name(name):
        """ Return a full template name """
        return 'simple_forums/notifications/emails/%s' % name

    def load_templates(self):
        """ Load templates for notification email """
        plain_temp = get_template(
            self._full_template_name('thread_update.txt'))
        plain = plain_temp.render(self._email_context())

        try:
            html_temp = get_template(
                self._full_template_name('thread_update.html'))
            html = html_temp.render(self._email_context())
        except TemplateDoesNotExist:
            html = None

        return (plain, html)

    def send_notification(self, message):
        """ Notify user that the given message has been posted """
        subject = 'Thread Updated'
        message = 'Thread #%d was updated' % self.thread.pk

        mail.send_mail(
            subject, message, 'no-reply@example.com',
            (self.user.email,), html_message=None)
