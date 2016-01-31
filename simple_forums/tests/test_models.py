from django.test import TestCase

from simple_forums import models


class TestMessageModel(TestCase):
	""" Tests for the message model """

	def test_create_with_all_fields(self):
		""" Test creation of a message with all its fields.

		A message instance should be able to be created with a body attribute.
		"""
		body = "Test body text"
		message = models.Message.objects.create(body=body)

		self.assertEqual(body, message.body)
