from django.core.urlresolvers import reverse

from simple_forums import models


def thread_detail_url(pk=None, thread=None):
    """ Get the url of a thread's detail view.

    Uses either the thread's pk or the thread instance itself to
    determine the url of the thread's detail view.
    """
    if pk is None and thread is None:
        raise ValueError("Either 'pk' or 'thread' must not be None")

    if pk:
        thread = models.Thread.objects.get(pk=pk)

    kwargs = {
        'topic_pk': thread.topic.pk,
        'topic_slug': thread.topic.slug,
        'thread_pk': thread.pk,
        'thread_slug': thread.slug,
    }

    return reverse('thread-detail', kwargs=kwargs)


def thread_list_url(topic_pk=None, topic=None):
    """ Get the url of the thread list view for a topic.

    Uses either the topic's pk or the topic instance itself to
    determine the url of the thread list view.
    """
    if topic_pk is None and topic is None:
        raise ValueError("Either 'topic_pk' or 'topic' must not be None")

    if topic_pk:
        topic = models.Topic.objects.get(pk=topic_pk)

    kwargs = {
        'topic_pk': topic.pk,
        'topic_slug': topic.slug,
    }

    return reverse('thread-list', kwargs=kwargs)
