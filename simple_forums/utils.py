import importlib

from django.conf import settings
from django.core.urlresolvers import reverse

from simple_forums import models


def get_setting(setting_name, default=None):
    """ Get the specified setting.

    If the setting exists, it will be returned. Otherwise, the default
    value will be returned.
    """
    settings_dict = getattr(settings, 'SIMPLE_FORUMS', None)

    if settings_dict:
        return settings_dict.get(setting_name, default)

    return default


def string_to_class(string):
    """ Return the class represented by the given string """
    module, class_name = string.rsplit('.', 1)

    return getattr(importlib.import_module(module), class_name)


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


def thread_list_url(topic_pk=None, topic=None, sort=None, rev=False):
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

    url = reverse('thread-list', kwargs=kwargs)

    args = []

    if sort:
        args.append('sort=%s' % sort)

    if rev is True:
        args.append('rev=true')

    if args:
        return '%s?%s' % (url, '&'.join(args))

    return url
