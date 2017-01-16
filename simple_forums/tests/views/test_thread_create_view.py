from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from simple_forums import models
from simple_forums.views import ThreadCreateView


# TODO: Figure out if these tests can be configured to not use the test
# client. The only reason we have to use the test client is to access
# context data on the responses.


def test_create_thread(admin_user, rf, topic_factory):
    """
    Test creating a new thread.

    Submitting valid data should create a new thread.
    """
    topic = topic_factory()
    data = {
        'topic': topic.pk,
        'title': 'Test Thread Title',
        'body': 'Test thread body.',
    }

    url = reverse('simple-forums:thread-create')
    request = rf.post(url, data)
    request.user = admin_user

    response = ThreadCreateView.as_view()(request)

    thread = models.Thread.objects.get()
    message = thread.message_set.get()

    assert response.status_code == 302
    assert response.url == thread.get_absolute_url()

    assert thread.title == data['title']
    assert message.body == data['body']


def test_empty_post(admin_client):
    """
    Test submitting an empty form.

    If an empty form is recieved, the user should be shown the same form
    with errors displayed.
    """
    url = reverse('simple-forums:thread-create')
    response = admin_client.post(url, {})

    assert response.status_code == 200

    form = response.context['form']

    assert form.is_bound
    assert not form.is_valid()


def test_get(admin_client):
    """
    Test sending a GET request to the view.

    A GET request to this view should display the form used to create a
    new thread.
    """
    url = reverse('simple-forums:thread-create')
    response = admin_client.get(url)

    assert response.status_code == 200

    form = response.context['form']

    assert not form.is_bound


def test_unauthenticated_request(rf):
    """
    Test the view as an unauthenticated user.

    If the user is unauthenticated, they should be redirected to the
    login page.
    """
    url = reverse('simple-forums:thread-create')

    request = rf.get(url)
    request.user = AnonymousUser()

    response = ThreadCreateView.as_view()(request)

    login_url = '{login}?next={next}'.format(login=settings.LOGIN_URL,
                                             next=url)

    assert response.status_code == 302
    assert response.url == login_url
