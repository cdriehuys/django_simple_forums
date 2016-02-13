from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from simple_forums import models
from simple_forums.tests.testing_utils import (
    create_message,
    create_thread,
    create_topic,)
from simple_forums.utils import thread_detail_url, thread_list_url


class AuthenticationTestCase(TestCase):
    """ Allows for easy authentication. """
    USERNAME = 'test'
    PASSWORD = 'test'

    def setUp(self, *args, **kwargs):
        """ Create a user for authentication. """
        self.user = get_user_model().objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD)

        return super(AuthenticationTestCase, self).setUp(*args, **kwargs)

    def assertLoginRedirect(self, response, next_url):
        """ Assert that the response redirects to the login url """
        login_url = '%s?next=%s' % (settings.LOGIN_URL, next_url)
        self.assertRedirects(response, login_url)

    def login(self):
        """ Log in the test client """
        self.client.login(
            username=self.USERNAME,
            password=self.PASSWORD)


class TestThreadCreateView(AuthenticationTestCase):
    """ Tests for ThreadCreateView """

    URL = reverse('thread-create')

    def test_empty_post(self):
        """ Test submitting empty form.

        If an empty form is submitted, the user should be redirected
        back to the thread creation form and errors should be shown.
        """
        self.login()

        response = self.client.post(self.URL, {})

        form = response.context['form']

        self.assertEqual(200, response.status_code)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_get(self):
        """ Test submitting a GET request to the view.

        A GET request to this view should display a form for creating a
        new thread.
        """
        self.login()

        response = self.client.get(self.URL)

        form = response.context['form']

        self.assertEqual(200, response.status_code)
        self.assertFalse(form.is_bound)

    def test_not_authenticated_get(self):
        """ Test unauthenticated user submitting a GET request.

        If a GET request is made by a user who is not authenticated,
        then they should be redirected to the login page.
        """
        response = self.client.get(self.URL)

        self.assertLoginRedirect(response, self.URL)

    def test_not_authenticated_post(self):
        """ Test unauthenticated user submitting a POST request.

        If a POST request is made by a user who is not authenticated,
        then they should be redirected to the login page.
        """
        response = self.client.post(self.URL, {})

        self.assertLoginRedirect(response, self.URL)

    def test_valid_form(self):
        """ Test authenticated user submitting a valid form.

        If an authenticated user submits a valid form, then a new
        thread should be created.
        """
        self.login()

        topic = create_topic()
        data = {
            'topic': '%d' % topic.pk,
            'title': 'Test Thread Title',
            'body': 'Test thread body',
        }

        response = self.client.post(self.URL, data)

        thread = models.Thread.objects.get()
        message = thread.message_set.get()

        self.assertRedirects(response, thread_detail_url(thread=thread))
        self.assertEqual(data['title'], thread.title)
        self.assertEqual(data['body'], message.body)


class TestThreadDetailView(TestCase):
    """ Tests for ThreadDetailView """

    def test_no_messages(self):
        """ Test the view when the given thread has no messages.

        If the thread has no messages, the response should contain a
        note to the user that there are no messages for the current
        thread.

        In practice, this should never occur because when threads are
        created, there should always be an initial message.
        """
        thread = create_thread()

        url = thread_detail_url(thread=thread)
        response = self.client.get(url)

        no_replies_message = "There are no replies to this thread"

        self.assertEqual(200, response.status_code)
        self.assertEqual(thread, response.context['thread'])
        self.assertContains(response, no_replies_message)

    def test_with_message(self):
        """ Test the view when the given thread has a message.

        If the thread has a message, it should be displayed following
        the thread's title.
        """
        thread = create_thread()
        message = create_message(thread=thread)

        url = thread_detail_url(thread=thread)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, message.body)


class TestThreadListView(TestCase):
    """ Tests for ThreadListView """

    def setUp(self):
        """ Create topic for testing """
        self.topic = create_topic()

    def test_no_threads(self):
        """ Test the view when there are no threads.

        If there are no threads, then the view should display a message
        that there are no threads.
        """
        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        empty_message = "No threads found"

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            [])
        self.assertContains(response, empty_message)

    def test_thread(self):
        """ Test view when there is a thread.

        If there is a thread, then the view should show the thread's
        name.
        """
        thread = create_thread(topic=self.topic)

        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        detail_url = thread_detail_url(thread=thread)
        href_text = 'href="%s"' % detail_url

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            ['<Thread: %s>' % thread.title])
        self.assertContains(response, thread.title)
        self.assertContains(response, href_text)

    def test_thread_for_different_topic(self):
        """ Test view when there is a thread for a different topic.

        If a thread is associated with a different topic, it should not
        be displayed.
        """
        thread = create_thread(topic=self.topic)
        create_thread(title="I shouldn't be included")

        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            ['<Thread: %s>' % thread])


class TestTopicListView(TestCase):
    """ Tests for TopicListView """

    URL = reverse('topic-list')

    def test_no_topics(self):
        """ Test the view when there are no topics.

        If there are no topics, a message should be displayed to
        inform the user that there are no topics.
        """
        response = self.client.get(self.URL)

        message = 'No topics found'

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['topic_list'],
            [])
        self.assertContains(response, message)

    def test_topic(self):
        """ Test the view when there is a topic.

        If there is a topic, it should be listed with its title and
        description.
        """
        topic = create_topic()

        response = self.client.get(self.URL)

        topic_url = thread_list_url(topic=topic)
        link_href = 'href="%s"' % topic_url

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['topic_list'],
            ['<Topic: %s>' % topic])
        self.assertContains(response, topic.title)
        self.assertContains(response, topic.description)
        self.assertContains(response, link_href)
