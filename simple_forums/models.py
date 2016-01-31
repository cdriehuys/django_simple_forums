from django.db import models


class Message(models.Model):
	""" A message with some text """

	body = models.TextField()

	def __str__(self):
		""" Return the message's body """
		return self.body
