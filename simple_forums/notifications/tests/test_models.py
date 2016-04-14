from django.core import mail
from django.test import TestCase

from simple_forums.notifications import models
from simple_forums.notifications.testing_utils import (
    create_thread_notification)
from simple_forums.tests.testing_utils import (
    create_message, create_thread, get_test_user)


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

    def test_email_context(self):
        """ Test getting the context used for emails.

        It should return a dictionary of the context used in the emails.
        """
        notification = create_thread_notification()

        expected = {}

        self.assertEqual(expected, notification._email_context())

    def test_load_email_templates(self):
        """ Test loading email templates for notifications.

        The method should find plaintext and html formats for the email.
        """
        notification = create_thread_notification()

        plain, html = notification.load_templates()

        self.assertIsNotNone(plain)
        self.assertIsNotNone(html)

    def test_send_notification(self):
        """ Test sending a notification email.

        Calling this method should send an email to the user assocated
        with the notification.
        """
        user = get_test_user(email='test@example.com')
        thread = create_thread()
        message = create_message(thread=thread)

        notification = models.ThreadNotification.objects.create(
            user=user,
            thread=thread)
        notification.send_notification(message)

        expected = 'Thread #%d was updated' % (thread.pk)

        self.assertEqual(1, len(mail.outbox))

        m = mail.outbox[0]

        self.assertEqual('Thread Updated', m.subject)
        self.assertEqual(expected, m.body)
        self.assertEqual('no-reply@example.com', m.from_email)
        self.assertEqual([user.email], m.to)

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
