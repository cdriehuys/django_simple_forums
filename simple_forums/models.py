from django.db import models


class Message(models.Model):
	""" A message with some text """

	body = models.TextField()
