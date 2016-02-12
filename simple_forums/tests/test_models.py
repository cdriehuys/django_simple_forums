from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from simple_forums import models
from simple_forums.tests.testing_utils import create_message, create_thread


class TestMessageModel(TestCase):
    """ Tests for the message model """

    def test_create_with_all_fields(self):
        """ Test creation of a message with all its fields.

        A message instance should be able to be created with a foreign
        key to a user instance, body text, and a time for its creation.
        """
        user = get_user_model().objects.create_user(
            username='test',
            password='test')
        thread = create_thread()
        body = "Test body text"
        time = timezone.now()

        message = models.Message.objects.create(
            user=user,
            thread=thread,
            body=body,
            time_created=time)

        self.assertEqual(user, message.user)
        self.assertEqual(thread, message.thread)
        self.assertEqual(body, message.body)
        self.assertEqual(time, message.time_created)

    def test_default_time_created(self):
        """ Test the default for the 'time_created' field.

        The field should default to the current time.
        """
        start_time = timezone.now()
        message = create_message()
        end_time = timezone.now()

        self.assertTrue(start_time <= message.time_created <= end_time)

    def test_string_conversion(self):
        """ Test the conversion of a message instance to a string.

        Converting a message instance to a string should return the
        message's body text.
        """
        message = models.Message(body="Test body text")

        self.assertEqual(message.body, str(message))


class TestThreadModel(TestCase):
    """ Tests for the thread model """

    def test_create_with_all_fields(self):
        """ Test creation of a thread with all its fields.

        A thread instance should be able to be created with title text.
        """
        time = timezone.now() - timedelta(days=1)

        thread = models.Thread.objects.create(
            title='test',
            time_created=time)

        self.assertEqual('test', thread.title)

    def test_num_replies_with_no_replies(self):
        """ Test retrieving the number of replies for a thread.

        If there are no messages associated with the thread, the number
        of replies should be 0.
        """
        thread = create_thread()

        self.assertEqual(0, thread.num_replies)

    def test_num_replies_with_reply(self):
        """ Test retrieving the number of replies for a thread.

        If there is a message associated with a thread, the number of
        replies should be 1.
        """
        thread = create_thread()
        create_message(thread=thread)

        self.assertEqual(1, thread.num_replies)

    def test_slug_generation(self):
        """ Test the automatic generation of a url slug.

        When creating a thread instance, the instance should generate a
        url slug based on its title.
        """
        thread = create_thread(title='test title')

        self.assertEqual('test-title', thread.slug)

    def test_slug_generation_for_long_title(self):
        """ Test generating a slug when the title is really long.

        If the title is longer than 50 characters, the slug should be
        truncated to 50 chars.
        """
        thread = create_thread(title='a' * 51)

        self.assertEqual('a' * 50, thread.slug)

    def test_string_conversion(self):
        """ Test converting a thread instance to a string.

        Converting a thread instance to a string should return the
        thread's title.
        """
        thread = models.Thread(title='test')

        self.assertEqual(thread.title, str(thread))
