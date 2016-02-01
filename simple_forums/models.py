from django.conf import settings
from django.db import models
from django.utils import timezone


class Message(models.Model):
    """ A message with some text """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    thread = models.ForeignKey('simple_forums.Thread')
    body = models.TextField()
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """ Return the message's body """
        return self.body


class Thread(models.Model):
    """ A thread with a title """

    title = models.CharField(max_length=200)

    def __str__(self):
        """ Return the thread's title """
        return self.title
