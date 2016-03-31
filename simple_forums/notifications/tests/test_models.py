from django.test import TestCase

from simple_forums.notifications import models
from simple_forums.tests.testing_utils import create_thread, get_test_user


class TestThreadNotificationModel(TestCase):
    """ Test model for handling thread notifications """

    def test_create(self):
        """ Test creating a new ThreadNotification.

        A ThreadNotification instance should be able to be created from
        a user and a thread.
        """

        thread = create_thread()
        user = get_test_user()

        notification = models.ThreadNotification.objects.create(
            user=user,
            thread=thread)

        self.assertEqual(1, models.ThreadNotification.objects.count())
        self.assertEqual(user, notification.user)
        self.assertEqual(thread, notification.thread)

    def test_string_conversion(self):
        """ Test converting a ThreadNotification instance to a string.

        Converting a ThreadNotification instance to a string should
        result in a string of the form:

        'Notify <user> of changes to thread #<id> (<thread title>)'
        """

        notification = models.ThreadNotification(
            user=get_test_user(),
            thread=create_thread())

        expected = 'Notify %s of changes to thread #%d (%s)' % (
            notification.user.username, notification.thread.id,
            notification.thread)

        self.assertEqual(expected, str(notification))
