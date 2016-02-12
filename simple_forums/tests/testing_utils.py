from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from simple_forums import models


def create_message(**kwargs):
    """ Create a message instance with the given arguments.

    Since this method is used for testing, it will create default
    values to pass to the instance.
    """

    user = kwargs.pop('user', None)
    thread = kwargs.pop('thread', None)
    body = kwargs.pop('body', 'test body')
    time_created = kwargs.pop('time_created', None)

    if len(kwargs) > 0:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    if user is None:
        user = get_user_model().objects.create_user(
            username='test',
            password='test')

    if thread is None:
        thread = create_thread()

    message_kwargs = dict(
        user=user,
        thread=thread,
        body=body)

    # Since this field has a default value defined in the model itself,
    # don't pass it if its value is None
    if time_created is not None:
        message_kwargs['time_created'] = time_created

    return models.Message.objects.create(**message_kwargs)


def create_thread(**kwargs):
    """ Create a thread instance for testing.

    Fills in default values for testing purposes.
    """

    topic = kwargs.pop('topic', None)
    title = kwargs.pop('title', 'test thread')
    time_created = kwargs.pop('time_created', None)

    if len(kwargs) > 0:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    if topic is None:
        topic = create_topic()

    thread_kwargs = dict(
        topic=topic,
        title=title)

    # Since this field has a default value defined in the model itself,
    # don't pass it if its value is None
    if time_created is not None:
        thread_kwargs['time_created'] = time_created

    return models.Thread.objects.create(**thread_kwargs)


def create_topic(**kwargs):
    """ Create topic instance for testing.

    Fills in default values for testing purposes.
    """

    title = kwargs.pop('title', 'test topic')
    description = kwargs.pop('description', 'test description')

    if len(kwargs) > 0:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    topic_kwargs = dict(
        title=title,
        description=description)

    return models.Topic.objects.create(**topic_kwargs)


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
