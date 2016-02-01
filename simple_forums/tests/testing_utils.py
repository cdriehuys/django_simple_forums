from django.contrib.auth import get_user_model

from simple_forums import models


def create_message(**kwargs):
    """ Create a message instance with the given arguments.

    Since this method is used for testing, it will create default
    values to pass to the instance.
    """

    user = kwargs.pop('user', None)
    body = kwargs.pop('body', 'test')
    time_created = kwargs.pop('time_created', None)

    if len(kwargs) > 0:
        raise ValueError(
            "Received unexpected kwargs: %s" % kwargs)

    if user is None:
        user = get_user_model().objects.create_user(
            username='test',
            password='test')

    message_kwargs = dict(
        user=user,
        body=body)

    if time_created is not None:
        message_kwargs['time_created'] = time_created

    return models.Message.objects.create(**message_kwargs)
