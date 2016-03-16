from datetime import timedelta
import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

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


class TestSearchView(TestCase):
    """ Tests for SearchView """

    URL = reverse('search')

    def test_no_query(self):
        """ Test requests with no query.

        If there is no query, then no search results should be
        displayed.
        """
        response = self.client.get(self.URL)

        self.assertEqual(200, response.status_code)
        self.assertTrue('query' not in response.context)

    def test_query(self):
        """ Test request with a query.

        If there is a query, the results for that query should be
        displayed.
        """
        thread = create_thread(title='test thread')

        url = '%s?q=%s' % (self.URL, 'test thread')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual('test thread', response.context['query'])
        self.assertQuerysetEqual(
            response.context['results'],
            ['<Thread: %s>' % thread])


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


class TestThreadDetailView(AuthenticationTestCase):
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

    def test_reply(self):
        """ Test submitting a valid reply.

        If a valid form is submitted, a new message should be created
        on the current thread.
        """
        self.login()

        thread = create_thread()
        data = {
            'body': 'Test body text.',
        }

        url = thread_detail_url(thread=thread)
        response = self.client.post(url, data)

        message = thread.message_set.get()

        self.assertRedirects(response, message.get_absolute_url())
        self.assertEqual(1, models.Message.objects.count())
        self.assertEqual(self.user, message.user)
        self.assertEqual(data['body'], message.body)

    def test_reply_empty(self):
        """ Test submitting an empty reply form.

        If an empty reply form is submitted, the user should be
        redirected back to the reply form, and an error should be
        displayed on the form.

        Regression test for #23
        """
        self.login()

        thread = create_thread()

        url = thread_detail_url(thread=thread)
        response = self.client.post(url, {})

        self.assertEqual(200, response.status_code)
        self.assertEqual(thread, response.context['thread'])

    def test_reply_unauthenticated(self):
        """ Test replying while unauthenticated.

        If an unauthenticated user tries to reply to a thread, an error
        should be shown.
        """
        thread = create_thread()
        data = {
            'body': 'Test body text.',
        }

        url = thread_detail_url(thread=thread)
        response = self.client.post(url, data)

        self.assertEqual(403, response.status_code)
        self.assertEqual(0, models.Message.objects.count())

    def test_reply_errors(self):
        """ Test submitting an invalid reply form.

        If an invalid reply is submitted, the reply form should be
        displayed with errors.
        """
        self.login()

        thread = create_thread()

        url = thread_detail_url(thread=thread)
        response = self.client.post(url, {})

        expected_errors = {
            'body': ['This field is required.'],
        }

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['reply_form'].is_bound)
        self.assertEqual(
            expected_errors,
            response.context['reply_form'].errors)

    def test_reply_form(self):
        """ Test presence of a reply form.

        If a user is logged in, there should be a reply form.
        """
        self.login()

        thread = create_thread()

        url = thread_detail_url(thread=thread)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['reply_form'].is_bound)

    def test_reply_form_unauthenticated(self):
        """ Test presence of reply form for unauthenticated users.

        If a user isn't logged in, there should be no reply form.
        """
        thread = create_thread()

        url = thread_detail_url(thread=thread)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTrue('reply_form' not in response.context)

    def test_with_message(self):
        """ Test the view when the given thread has a message.

        If the thread has a message, it should be displayed following
        the thread's title.
        """
        thread = create_thread()
        message = create_message(user=self.user, thread=thread)

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

    def test_sort_invalid_parameter(self):
        """ Test behavior when an invalid sort value is used.

        If the sorting method is invalid, the default sorting order
        should be used (i.e. last activity time).
        """
        past = timezone.now() - timedelta(days=1)

        thread1 = create_thread(
            topic=self.topic,
            title='thread 1',
            time_created=past)
        thread2 = create_thread(
            topic=self.topic,
            title='thread 2')

        url = thread_list_url(topic=self.topic, sort='foo')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            ['<Thread: %s>' % thread2, '<Thread: %s>' % thread1])

    def test_sort_title(self):
        """ Test sorting by title field.

        If the request has a GET variable of 'sort' with the value of
        'title', then the threads should be ordered by title.
        """
        thread1 = create_thread(
            topic=self.topic,
            title='cats')
        thread2 = create_thread(
            topic=self.topic,
            title='animals')
        thread3 = create_thread(
            topic=self.topic,
            title='bats')

        url = thread_list_url(topic=self.topic, sort='title')
        response = self.client.get(url)

        expected = [
            '<Thread: %s>' % thread2,
            '<Thread: %s>' % thread3,
            '<Thread: %s>' % thread1,
        ]

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            expected)

    def test_sort_context(self):
        """ Test default context pertaining to sorting.

        By default, the sort_options should include all the fields by
        which the threads are sortable. The context should also include
        the current sort field and if the sort order is reversed.
        """
        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        expected_sort_options = ['activity', 'title']

        self.assertEqual(200, response.status_code)

        # Assert lists equal for both python 2 and 3
        if sys.version_info[0] < 3:
            self.assertItemsEqual(
                expected_sort_options,
                response.context['sort_options'])
        else:
            self.assertCountEqual(
                expected_sort_options,
                response.context['sort_options'])

        self.assertEqual(
            'activity',
            response.context['sort_current'])
        self.assertTrue(response.context['sort_reversed'])

    def test_sort_title_reversed(self):
        """ Test sorting by title field reversed.

        If the request has a GET variable of 'sort' with the value of
        'title', and a variable 'reverse' with the value of 'true',
        then the threads should be ordered by title in reverse
        alphabetical order.
        """
        thread1 = create_thread(
            topic=self.topic,
            title='cats')
        thread2 = create_thread(
            topic=self.topic,
            title='animals')
        thread3 = create_thread(
            topic=self.topic,
            title='bats')

        url = thread_list_url(topic=self.topic, sort='title', rev=True)
        response = self.client.get(url)

        expected = [
            '<Thread: %s>' % thread1,
            '<Thread: %s>' % thread3,
            '<Thread: %s>' % thread2,
        ]

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            expected)

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

    def test_threads(self):
        """ Test view with multiple threads.

        If there are multiple threads, they should be ordered by the
        date of their last activity.
        """
        past = timezone.now() - timedelta(days=1)
        thread1 = create_thread(
            topic=self.topic,
            title='Test Thread 1',
            time_created=past)
        thread2 = create_thread(
            topic=self.topic,
            title='Test Thread 2')

        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            ['<Thread: %s>' % thread2, '<Thread: %s>' % thread1])

    def test_topic_context(self):
        """ Test passing the topic as a context variable.

        This view should have the parent topic as a context variable.
        """
        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.topic, response.context['topic'])

    def test_sticky_thread(self):
        """ Test view when there is a sticky thread.

        If there is a sticky thread, it should be in a context variable
        for the sticky threads, and not in the one for normal threads.
        """
        thread = create_thread(topic=self.topic)
        sticky_thread = create_thread(
            topic=self.topic,
            title='Sticky Thread',
            sticky=True)

        url = thread_list_url(topic=self.topic)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            ['<Thread: %s>' % thread])
        self.assertQuerysetEqual(
            response.context['sticky_thread_list'],
            ['<Thread: %s>' % sticky_thread])


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
