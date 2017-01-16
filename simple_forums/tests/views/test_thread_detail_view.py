from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

import pytest

from simple_forums import models
from simple_forums.views import ThreadDetailView


def test_message(rf, message_factory):
    """
    Test the view when the thread has a message set.

    If the thread has a message, it should be displayed.
    """
    message = message_factory()

    url = message.thread.get_absolute_url()
    request = rf.get(url)
    request.user = AnonymousUser()

    response = ThreadDetailView.as_view()(request, thread_pk=message.thread.pk)

    response.render()

    assert response.status_code == 200
    assert message.body in response.content.decode(response.charset)


def test_no_messages(rf, thread_factory):
    """
    Test viewing the details of a thread with no replies.

    If the thread has no messages, the response should contain a
    message informing the user that there are no replies.
    """
    thread = thread_factory()

    url = thread.get_absolute_url()
    request = rf.get(url)
    request.user = AnonymousUser()

    response = ThreadDetailView.as_view()(request, thread_pk=thread.pk)

    no_replies_message = 'There are no replies to this thread'

    response.render()

    assert response.status_code == 200
    assert no_replies_message in response.content.decode(response.charset)


def test_reply(admin_user, rf, thread_factory):
    """
    Test submitting a reply.

    If a valid reply form is submitted, a new message should be created
    on the current thread.
    """
    thread = thread_factory()
    data = {
        'body': 'Test message body.',
    }

    url = thread.get_absolute_url()
    request = rf.post(url, data)
    request.user = admin_user

    response = ThreadDetailView.as_view()(request, thread_pk=thread.pk)

    message = thread.message_set.get()

    assert response.status_code == 302
    assert response.url == message.get_absolute_url()

    assert models.Message.objects.count() == 1
    assert message.user == admin_user
    assert message.body == data['body']


def test_reply_empty(admin_user, rf, thread_factory):
    """
    Test submitting an empty reply.

    If an empty reply form is submitted, the reply form should be
    displayed again.
    """
    thread = thread_factory()

    url = thread.get_absolute_url()
    request = rf.post(url, {})
    request.user = admin_user

    response = ThreadDetailView.as_view()(request, thread_pk=thread.pk)

    assert response.status_code == 200


def test_reply_form(admin_client, thread_factory):
    """
    Test the presence of a reply form.

    If an authenticated user views the page, a reply form should be
    present.
    """
    thread = thread_factory()

    url = thread.get_absolute_url()
    response = admin_client.get(url)

    assert response.status_code == 200
    assert not response.context['reply_form'].is_bound


def test_reply_form_unauthenticated(client, thread_factory):
    """
    Test presence of a reply form for unauthenticated users.

    If an unauthenticated user views the page, a reply form should not
    be displayed.
    """
    thread = thread_factory()

    url = thread.get_absolute_url()
    response = client.get(url)

    assert response.status_code == 200
    assert 'reply_form' not in response.context


def test_reply_unauthenticated(admin_user, rf, thread_factory):
    """
    Test replying while unauthenticated.

    If an unauthenticated user tries to reply to a thread, a 403
    response should be returned.
    """
    thread = thread_factory()

    url = thread.get_absolute_url()
    request = rf.post(url, {'body': 'Test body text.'})
    request.user = AnonymousUser()

    with pytest.raises(PermissionDenied):
        ThreadDetailView.as_view()(request, thread_pk=thread.pk)
