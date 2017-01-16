from datetime import timedelta

from django.utils import timezone

from simple_forums.models import Message


def test_create(thread_factory, usr_factory):
    """
    Test creating a new message.

    A message should be creatable with a user, thread, body, and
    creation time.
    """
    body = 'Test message body.'
    thread = thread_factory()
    time_created = timezone.now()
    user = usr_factory()

    Message.objects.create(
        body=body,
        thread=thread,
        time_created=time_created,
        user=user)


def test_get_absolute_url(message_factory):
    """
    Test getting the url of a message.

    The url should include both the url of the message's thread as well
    as the message's anchor.
    """
    message = message_factory()
    expected = '{url}#{anchor}'.format(
        anchor=message.get_anchor(),
        url=message.thread.get_absolute_url())

    assert message.get_absolute_url() == expected


def test_get_anchor(message_factory):
    """
    Test getting the anchor tag of a message.

    The anchor should include a prefix and the message's id.
    """
    message = message_factory()
    expected = 'm-{id}'.format(id=message.id)

    assert message.get_anchor() == expected


def test_string_conversion(message_factory):
    """
    Test converting a message to a string.

    Converting a message to a string should return a string that says
    which thread the message is in, as well as the ID of the message.
    """
    message = message_factory()
    expected = 'Message in {thread} (ID {id})'.format(
        id=message.id,
        thread=message.thread)

    assert str(message) == expected


def test_update_thread_activity_time(message_factory, thread_factory):
    """
    Test updating a message's thread's activity time.

    When a message is saved, it should update its parent thread's
    ``time_last_activity`` attribute.
    """
    now = timezone.now()
    past = now - timedelta(days=1)
    thread = thread_factory(time_last_activity=past)
    message = message_factory(thread=thread, time_created=now)

    assert message.thread.time_last_activity == message.time_created
