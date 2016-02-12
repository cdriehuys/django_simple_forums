from django.contrib.auth import get_user_model
from django.test import TestCase

from simple_forums import forms, models
from simple_forums.tests.testing_utils import create_topic


class TestThreadCreationForm(TestCase):
    """ Test the form used to create new threads """

    def test_empty(self):
        """ Test validation of an empty form.

        If the form is empty, it should return errors about all the
        required fields.
        """
        form = forms.ThreadCreationForm({})

        expected_errors = {
            'topic': ['This field is required.'],
            'title': ['This field is required.'],
            'body': ['This field is required.'],
        }

        self.assertFalse(form.is_valid())
        self.assertEqual(expected_errors, form.errors)

    def test_save(self):
        """ Test saving the form.

        Saving the form should create a new thread from the title field
        in the form, and a new message on that thread containing the
        body field from the form.
        """
        topic = create_topic()
        data = {
            'topic': '%d' % topic.pk,
            'title': 'Test thread title',
            'body': 'Test message body',
        }
        form = forms.ThreadCreationForm(data)
        user = get_user_model().objects.create_user(
            username='test',
            password='test')

        form.save(user)

        self.assertEqual(1, models.Thread.objects.count())
        self.assertEqual(1, models.Message.objects.count())

        thread = models.Thread.objects.get()
        message = models.Message.objects.get()

        self.assertEqual(data['title'], thread.title)
        self.assertEqual(user, message.user)
        self.assertEqual(thread, message.thread)
        self.assertEqual(data['body'], message.body)
