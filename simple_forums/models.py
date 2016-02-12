from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


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

    topic = models.ForeignKey('Topic')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """ Return the thread's title """
        return self.title

    @property
    def num_replies(self):
        return self.message_set.count()

    def save(self, *args, **kwargs):
        """ Save the thread instance

        Overriden to generate a url slug.
        """
        # Only create the slug if this is a new object.
        # Changing existing slugs would create dead links.
        if not self.id:
            # Slugify and truncate to 50 characters
            self.slug = slugify(self.title)[:50]

        return super(Thread, self).save(*args, **kwargs)

    @property
    def time_last_activity(self):
        """ Return the time of the last activity on the thread.

        If the thread has no replies, this method returns the time of
        this thread's creation. If there are replies, it returns the
        time of the most recent message.
        """
        if self.num_replies:
            messages = self.message_set.order_by('-time_created')
            return messages.first().time_created

        return self.time_created


class Topic(models.Model):
    """ A topic model to hold threads """

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        """ Return the topic's title """
        return self.title

    def save(self, *args, **kwargs):
        """ Save the topic instance

        Overriden to generate a url slug.
        """
        # Only create the slug if this is a new object.
        # Changing existing slugs would create dead links.
        if not self.id:
            # Slugify and truncate to 50 characters
            self.slug = slugify(self.title)[:50]

        return super(Topic, self).save(*args, **kwargs)
