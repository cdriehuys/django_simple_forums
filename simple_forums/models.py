from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from adminsortable.models import SortableMixin


class Message(models.Model):
    """ A message with some text """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    thread = models.ForeignKey('simple_forums.Thread')
    body = models.TextField()
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """ Return the message's body """
        return self.body

    def get_absolute_url(self):
        """ Return the url of the message instance """
        return '%s#%s' % (self.thread.get_absolute_url(), self.get_anchor())

    def get_anchor(self):
        """ Get the anchor for the message """
        return 'm-%d' % self.pk

    def get_search_description(self):
        """ Return description of message for search results """
        return '%s said: %s' % (self.user, self.body)

    def get_title(self):
        """ Return the parent thread's title """
        return self.thread.get_title()

    def save(self, *args, **kwargs):
        """ Update the parent thread's 'time_last_activity' field """
        if self.time_created > self.thread.time_last_activity:
            self.thread.time_last_activity = self.time_created
            self.thread.save()

        return super(Message, self).save(*args, **kwargs)


class Thread(models.Model):
    """ A thread with a title """

    topic = models.ForeignKey('Topic')
    title = models.CharField(max_length=200)
    sticky = models.BooleanField(default=False)
    slug = models.SlugField()
    time_created = models.DateTimeField(default=timezone.now)
    time_last_activity = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        """ Initialize 'time_last_activity' to 'time_created' """
        super(Thread, self).__init__(*args, **kwargs)

        self.time_last_activity = self.time_created

    def __str__(self):
        """ Return the thread's title """
        return self.title

    def get_absolute_url(self):
        """ Return the url of the instance's detail view """
        url_kwargs = {
            'topic_pk': self.topic.pk,
            'topic_slug': self.topic.slug,
            'thread_pk': self.pk,
            'thread_slug': self.slug,
        }

        return reverse('thread-detail', kwargs=url_kwargs)

    def get_search_description(self):
        """ Return description of thread for search results """
        if self.message_set.exists():
            return self.message_set.first().body

        return 'There are no replies to this thread.'

    def get_title(self):
        """ Return the thread's title """
        return self.title

    @property
    def num_replies(self):
        """ Get the number of replies to the thread """
        count = self.message_set.count()

        if not count:
            return count

        return count - 1

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


class Topic(SortableMixin):
    """ A topic model to hold threads """

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    slug = models.SlugField()

    # field used by django-admin-sortable for ordering topics
    topic_order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True)

    class Meta:
        ordering = ('topic_order',)

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
