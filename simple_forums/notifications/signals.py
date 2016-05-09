from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_forums.notifications import models


@receiver(post_save, sender='simple_forums.Message')
def send_notifications(sender, instance, created, *args, **kwargs):
    """ Notify users that a reply has been posted """
    if created:
        message = instance
        thread = message.thread
        for n in models.ThreadNotification.objects.filter(thread=thread):
            if n.user != message.user:
                n.send_notification(message)
