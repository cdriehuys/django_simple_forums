from django.core import mail
from django.test import TestCase

from simple_forums.notifications.testing_utils import (
    create_thread_notification)
from simple_forums.tests.testing_utils import (
    create_message, create_thread, get_test_user)


class MailTestMixin:

    def assertMailEqual(self, expected, actual):
        assert expected.subject == actual.subject
        assert expected.body == actual.body
        assert expected.from_email == actual.from_email
        assert expected.to == actual.to


class TestThreadNotificationSignal(TestCase, MailTestMixin):
    """ Test signal used to update users of a reply to a thread """

    def test_create_new_message(self):
        """ Test creating a new message.

        Creating a new message on a thread that has a notification
        associated with it should send an email notification.
        """
        user = get_test_user()
        thread = create_thread()
        notification = create_thread_notification(
            user=user, thread=thread)

        message = create_message(
            user=get_test_user(username="test2"),
            thread=thread)

        self.assertEqual(1, len(mail.outbox))

        result = mail.outbox[0]

        mail.outbox = []

        notification.send_notification(message)
        expected = mail.outbox[0]

        self.assertMailEqual(expected, result)

    def test_self_notification(self):
        """ Test user replying to watched thread.

        If a user is receiving notifications for a thread, they should
        not receive a notification if they were the one who posted a
        reply.
        """
        user = get_test_user()
        thread = create_thread()

        create_thread_notification(
            user=user, thread=thread)

        create_message(user=user, thread=thread)

        self.assertEqual(0, len(mail.outbox))

    def test_update_message(self):
        """ Test updating an existing message.

        Updating an existing message should not trigger a new
        notification.
        """
        user = get_test_user()
        thread = create_thread()
        message = create_message(thread=thread)
        create_thread_notification(
            user=user, thread=thread)

        message.body = "New body text"
        message.save()

        self.assertEqual(0, len(mail.outbox))
