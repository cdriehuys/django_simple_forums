import pytest
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify

from simple_forums.models import Topic


@pytest.mark.django_db
def test_create():
    """
    Test creating a new topic.

    Test passing in all available fields.
    """
    Topic.objects.create(
        description='Test topic description.',
        title='Test Topic')


def test_get_absolute_url(topic_factory):
    """
    Test getting the url of a topic.

    The method should return the url of the topic's detail view.
    """
    topic = topic_factory()
    expected = reverse('simple-forums:thread-list', kwargs={
        'topic_pk': topic.pk,
        'topic_slug': topic.slug,
    })

    assert topic.get_absolute_url() == expected


def test_last_thread(msg_factory, thread_factory, topic_factory):
    """
    Test the ``last_thread`` property with multiple threads.

    If there are multiple threads, ``last_thread`` should return the
    thread with the most recent ``time_last_activity``.
    """
    topic = topic_factory()

    past = timezone.now() - timedelta(days=1)
    far_past = past - timedelta(days=1)

    thread = thread_factory(time_created=past, topic=topic)
    msg_factory(thread=thread)

    thread_factory(time_created=far_past, topic=topic)

    assert topic.last_thread == thread


def test_last_thread_no_threads(topic_factory):
    """
    Test the ``last_thread`` property with no threads.

    If a topic has no threads, ``last_thread`` should equal ``None``.
    """
    topic = topic_factory()

    assert topic.last_thread is None


def test_order(topic_factory):
    """
    Test ordering of topics.

    Topics should be ordered by the ``topic_order`` field.
    """
    topic_factory()
    topic_factory()
    topic_factory()

    expected = [t for t in Topic.objects.order_by('topic_order')]

    assert list(Topic.objects.all()) == expected


def test_slug_generation(topic_factory):
    """
    Test automatic generation of slugs for topics.

    When a topic is created, a slug should be generated from its title.
    """
    title = 'This Is A Really Long Title So We Can Test Slug Truncation'
    topic = topic_factory(title=title)

    expected = slugify(topic.title)[:50]

    assert topic.slug == expected


def test_slug_title_change(topic_factory):
    """
    Test slug behavior when a topic's title changes.

    If a topic's title changes, its slug should not change.
    """
    topic = topic_factory()
    slug = topic.slug

    topic.title = 'My New Awesome Title'
    topic.save()

    assert topic.slug == slug


def test_string_conversion(topic_factory):
    """
    Test converting a topic to a string.

    Converting a topic to a string should return the topic's title.
    """
    topic = topic_factory()

    assert str(topic) == topic.title
