from django.core.urlresolvers import reverse
from django.test import TestCase

from simple_forums import models
from simple_forums.testing_utils import (
    create_message,
    create_thread,
    create_topic)


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
