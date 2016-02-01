from django.conf import settings
from django.db import models
from django.utils import timezone


class Message(models.Model):
    """ A message with some text """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    body = models.TextField()
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """ Return the message's body """
        return self.body
