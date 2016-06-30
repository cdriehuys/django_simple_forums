from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from simple_forums.notifications import models
from simple_forums.notifications.testing_utils import (
    create_thread_notification)
from simple_forums.tests.testing_utils import create_thread
from simple_forums.utils import thread_detail_url


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

    def login(self):
        """ Log in the test client """
        self.client.login(
            username=self.USERNAME,
            password=self.PASSWORD)


class TestThreadNotificationView(AuthenticationTestCase):
    """ Test view used to create/destroy new thread notifications """

    def test_delete(self):
        """ Test unfollowing a thread.

        If the 'follow' variable is false, the ThreadNotification
        instance for the current thread and user should be deleted.
        """
        self.login()

        thread = create_thread()
        create_thread_notification(
            user=self.user, thread=thread)

        data = {}

        success_url = thread_detail_url(thread=thread)

        url = reverse('simple-forums:follow-thread', kwargs={'pk': thread.pk})
        response = self.client.post(url, data)

        self.assertRedirects(response, success_url)
        self.assertEqual(0, models.ThreadNotification.objects.count())

    def test_duplicate_request(self):
        """ Test trying to create a duplicate notification instance.

        If a user already has notifications set up for a thread and they
        try to create another notification instance, nothing should
        happen.
        """
        self.login()

        thread = create_thread()
        create_thread_notification(
            user=self.user, thread=thread)

        data = {'follow': 'on'}

        success_url = thread_detail_url(thread=thread)

        url = reverse('simple-forums:follow-thread', kwargs={'pk': thread.pk})
        response = self.client.post(url, data)

        self.assertRedirects(response, success_url)
        self.assertEqual(1, models.ThreadNotification.objects.count())

    def test_get(self):
        """ Test a GET request.

        GET requests should not be allowed and should return a 405
        status code.
        """
        self.login()

        thread = create_thread()

        url = reverse('simple-forums:follow-thread', kwargs={'pk': thread.pk})
        response = self.client.get(url)

        self.assertEqual(405, response.status_code)

    def test_post_unauthenticated(self):
        """ Test sending an unauthenticated POST request.

        A POST request from an unauthenticated user should result in a
        403 status code.
        """
        thread = create_thread()

        url = reverse('simple-forums:follow-thread', kwargs={'pk': thread.pk})
        response = self.client.post(url, {})

        self.assertEqual(403, response.status_code)

    def test_post_valid_follow(self):
        """ Test POSTing valid data.

        If a POST request with valid data is submitted, a new
        ThreadNotification instance should be created.
        """
        self.login()

        thread = create_thread()
        data = {'follow': 'on'}
        success_url = thread_detail_url(thread=thread)

        url = reverse('simple-forums:follow-thread', kwargs={'pk': thread.pk})
        response = self.client.post(url, data)

        self.assertRedirects(response, success_url)
        self.assertEqual(1, models.ThreadNotification.objects.count())
        self.assertEqual(
            self.user, models.ThreadNotification.objects.get().user)
        self.assertEqual(
            thread, models.ThreadNotification.objects.get().thread)
