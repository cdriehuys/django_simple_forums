from django.test import TestCase

from simple_forums import forms


class TestThreadCreationForm(TestCase):
    """ Test the form used to create new threads """

    def test_empty(self):
        """ Test validation of an empty form.

        If the form is empty, it should return errors about all the
        required fields.
        """
        form = forms.ThreadCreationForm({})

        expected_errors = {
            'title': ['This field is required.'],
            'body': ['This field is required.'],
        }

        self.assertFalse(form.is_valid())
        self.assertEqual(expected_errors, form.errors)
