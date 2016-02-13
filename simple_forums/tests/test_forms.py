from django.contrib.auth import get_user_model
from django.test import TestCase

from simple_forums import forms, models
from simple_forums.tests.testing_utils import create_thread, create_topic


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

    def test_save_invalid_data(self):
        """ Test attempting to save an invalid form.

        Trying to save a form with invalid data should not create a new
        thread.
        """
        data = {
            'foo': 'bar',
            'bar': 'foo',
        }
        form = forms.ThreadCreationForm(data)

        user = get_user_model().objects.create_user(
            username='test',
            password='test')

        form.save(user)

        self.assertEqual(0, models.Thread.objects.count())
        self.assertEqual(0, models.Message.objects.count())


class TestThreadReplyForm(TestCase):
    """ Tests for form used to reply to threads """

    def test_empty(self):
        """ Test validating an empty form.

        If the form is empty, errors should be raised for each required
        field.
        """
        form = forms.ThreadReplyForm({})

        expected_errors = {
            'body': ['This field is required.'],
        }

        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(expected_errors, form.errors)

    def test_save(self):
        """ Test saving a valid form.

        Saving a valid form should create a new reply on the given
        thread.
        """
        user = get_user_model().objects.create_user(
            username='test',
            password='test')
        thread = create_thread()

        data = {
            'body': 'Test body text.',
        }

        form = forms.ThreadReplyForm(data)
        message = form.save(user, thread)

        self.assertEqual(1, thread.message_set.count())
        self.assertEqual(data['body'], message.body)

    def test_save_invalid_data(self):
        """ Test trying to save invalid data.

        Trying to save a form with invalid data should not create a new
        message.
        """
        user = get_user_model().objects.create_user(
            username='test',
            password='test')
        thread = create_thread()

        form = forms.ThreadReplyForm({})
        form.save(user, thread)

        self.assertEqual(0, models.Message.objects.count())
