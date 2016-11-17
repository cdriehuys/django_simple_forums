from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify

from simple_forums.models import Thread


def test_create(topic_factory):
    """
    Test creating a new thread.

    Passing in all the possible allowed fields should create a new
    thread.
    """
    params = {
        'sticky': True,
        'time_created': timezone.now(),
        'time_last_activity': timezone.now(),
        'title': 'Test Thread',
        'topic': topic_factory(),
    }

    Thread.objects.create(**params)


def test_default_time_last_activity(thread_factory):
    """
    Test the default value of ``time_last_activity``.

    By default, ``time_last_activity`` should equal the thread's
    ``time_created`` attribute.
    """
    thread = thread_factory(time_last_activity=None)

    assert thread.time_last_activity == thread.time_created


def test_get_absolute_url(thread_factory):
    """
    Test getting the url of a thread.

    The method should return the url of the thread's detail view.
    """
    thread = thread_factory()
    expected = reverse('simple-forums:thread-detail', kwargs={
        'thread_pk': thread.pk,
        'thread_slug': thread.slug,
        'topic_pk': thread.topic.pk,
        'topic_slug': thread.topic.slug,
    })

    assert thread.get_absolute_url() == expected


def test_num_replies_initial_message(msg_factory, thread_factory):
    """
    Test ``num_replies`` with the initial message.

    The initial message should not count toward the number of replies.
    """
    thread = thread_factory()
    # Create initial message
    msg_factory(thread=thread)

    assert thread.num_replies == 0


def test_num_replies_multiple_messages(msg_factory, thread_factory):
    """
    Test ``num_replies`` with multiple replies.

    All messages after the initial one should count toward the number
    of replies.
    """
    thread = thread_factory()
    # Initial message
    msg_factory(thread=thread)
    # Additional messages should apply toward the count
    msg_factory(thread=thread)
    msg_factory(thread=thread)

    expected = thread.message_set.count() - 1

    assert thread.num_replies == expected


def test_num_replies_no_messages(thread_factory):
    """
    Test ``num_replies`` with no messages.

    If there are no messages associated with a thread, ``num_replies``
    should be 0.
    """
    thread = thread_factory()

    assert thread.num_replies == 0


def test_slug_generation(thread_factory):
    """
    Test automatic slug generation for a thread.

    The slug for a thread should be the slugified version of its title.
    """
    title = 'This Thread has a Really Long Title so We Can Test Truncation'
    thread = thread_factory(title=title)

    assert thread.slug == slugify(thread.title)[:50]


def test_slug_with_title_change(thread_factory):
    """
    Test slug generation with a modified title.

    If a thread's title changes, it's slug should not change.
    """
    thread = thread_factory()
    slug = thread.slug

    thread.title = 'My New Awesome Title'
    thread.save()

    assert thread.slug == slug


def test_string_conversion(thread_factory):
    """
    Test converting a thread to a string.

    Converting a thread to a string should return the thread's title.
    """
    thread = thread_factory()

    assert str(thread) == thread.title
