from django.test import TestCase
from django.utils import timezone

from simple_forums import models


class TestMessageModel(TestCase):
	""" Tests for the message model """

	def test_create_with_all_fields(self):
		""" Test creation of a message with all its fields.

		A message instance should be able to be created with a body attribute.
		"""
		body = "Test body text"
		time = timezone.now()

		message = models.Message.objects.create(
			body=body,
			time_created=time
		)

		self.assertEqual(body, message.body)

	def test_default_time_created(self):
		""" Test the default for the 'time_created' field.

		The field should default to the current time.
		"""
		start_time = timezone.now()
		message = models.Message.objects.create(body='test')
		end_time = timezone.now()

		self.assertTrue(start_time <= message.time_created <= end_time)

	def test_string_conversion(self):
		""" Test the conversion of a message instance to a string.

		Converting a message instance to a string should return the message's
		body text.
		"""
		message = models.Message(body="Test body text")

		self.assertEqual(message.body, str(message))
