from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from simple_forums import models
from simple_forums.testing_utils import (
    create_message,
    create_thread,
    create_topic)


class TestThreadModel(TestCase):
    """ Tests for the thread model """

    def test_create_with_all_fields(self):
        """ Test creation of a thread with all its fields.

        A thread instance should be able to be created with title text.
        """
        topic = create_topic()
        time = timezone.now() - timedelta(days=1)

        thread = models.Thread.objects.create(
            topic=topic,
            title='test',
            time_created=time)

        self.assertEqual(topic, thread.topic)
        self.assertEqual('test', thread.title)
        self.assertEqual(time, thread.time_created)

    def test_default_time_created(self):
        """ Test the default for the 'time_created' field.

        If no parameter is passed to 'time_created', it should default
        to the current time.
        """
        start_time = timezone.now()
        thread = create_thread()
        end_time = timezone.now()

        self.assertTrue(start_time <= thread.time_created <= end_time)

    def test_get_absolute_url(self):
        """ Test getting the url of a thread instance.

        This method should return the url of the instance's detail
        view.
        """
        thread = create_thread()

        url_kwargs = {
            'topic_pk': thread.topic.pk,
            'topic_slug': thread.topic.slug,
            'thread_pk': thread.pk,
            'thread_slug': thread.slug,
        }
        url = reverse('simple-forums:thread-detail', kwargs=url_kwargs)

        self.assertEqual(url, thread.get_absolute_url())

    def test_get_title(self):
        """ Test getting the thread's title.

        This method should return the title field of the thread.
        """
        thread = create_thread()

        self.assertEqual(thread.title, thread.get_title())

    def test_num_replies_with_no_replies(self):
        """ Test retrieving the number of replies for a thread.

        If there are no messages associated with the thread, the number
        of replies should be 0.
        """
        thread = create_thread()

        self.assertEqual(0, thread.num_replies)

    def test_num_replies_with_initial_reply(self):
        """ Test retrieving the number of replies for a thread.

        If the only message associated with a thread is the initial
        message, then the property should return 0 replies.
        """
        thread = create_thread()
        create_message(thread=thread)

        self.assertEqual(0, thread.num_replies)

    def test_num_replies_with_more_replies(self):
        """ Test retrieving the number of replies for a thread.

        If the thread has a message that is not the initial message,
        then the property should return the number of additional
        messages.
        """
        thread = create_thread()
        # simulate inital message
        create_message(thread=thread)

        # create additional message
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

    def test_sticky_default(self):
        """ Test default 'sticky' value.

        Threads should not be sticky by default.
        """
        thread = create_thread()

        self.assertFalse(thread.sticky)

    def test_string_conversion(self):
        """ Test converting a thread instance to a string.

        Converting a thread instance to a string should return the
        thread's title.
        """
        thread = models.Thread(title='test')

        self.assertEqual(thread.title, str(thread))

    def test_time_last_activity_no_replies(self):
        """ Test the 'time_last_activity' property with no replies.

        If there are no replies, this property should return the time
        that the thread was created.
        """
        thread = create_thread()

        self.assertEqual(thread.time_created, thread.time_last_activity)

    def test_time_last_activity_with_reply(self):
        """ Test the 'time_last_activity' property with a reply.

        If there is a reply, this property should return the time that
        the most recent reply was posted.
        """
        past = timezone.now() - timedelta(days=1)
        thread = create_thread(time_created=past)
        message = create_message(thread=thread)

        self.assertEqual(message.time_created, thread.time_last_activity)


class TestTopicModel(TestCase):
    """ Tests for the topic model """

    def test_create_with_all_fields(self):
        """ Test creating a topic with all of its fields specified. """
        title = 'thread title'
        description = 'thread description'

        topic = models.Topic.objects.create(
            title=title,
            description=description)

        self.assertEqual(title, topic.title)
        self.assertEqual(description, topic.description)

    def test_last_thread(self):
        """ Test getting a topic's most recently active thread.

        If a topic has multiple threads, the method should return the
        most recently active one.
        """
        topic = create_topic()

        # create and populate first thread
        thread = create_thread(topic=topic)
        create_message(thread=thread)

        # create and populate second thread
        thread2 = create_thread(topic=topic, title="thread 2")
        create_message(thread=thread2)

        self.assertEqual(thread2, topic.last_thread)

    def test_get_absolute_url(self):
        """Test getting a Topic instance's absolute url.

        It should return the url of the thread list view for the topic.
        """
        topic = create_topic()

        expected = reverse('simple-forums:thread-list', kwargs={
            'topic_pk': topic.pk,
            'topic_slug': topic.slug,
        })

        self.assertEqual(expected, topic.get_absolute_url())

    def test_last_thread_with_no_threads(self):
        """ Test getting a topic's most recently active thread.

        If there are no threads associated with a topic, then
        'last_thread' should be None.
        """
        topic = create_topic()

        self.assertIsNone(topic.last_thread)

    def test_slug_generation(self):
        """ Test the automatic generation of a url slug.

        When creating a topic instance, the instance should generate a
        url slug based on its title.
        """
        topic = create_topic(title='test title')

        self.assertEqual('test-title', topic.slug)

    def test_slug_generation_for_long_title(self):
        """ Test generating a slug when the title is really long.

        If the title is longer than 50 characters, the slug should be
        truncated to 50 chars.
        """
        topic = create_topic(title='a' * 51)

        self.assertEqual('a' * 50, topic.slug)

    def test_string_conversion(self):
        """ Test converting a topic instance to a string.

        Converting a topic instance to a string should return the
        topic's title.
        """
        topic = models.Topic(title='test')

        self.assertEqual(topic.title, str(topic.title))
