from django.contrib.auth import get_user_model

from simple_forums import models


def create_message(**kwargs):
    """ Create a message instance with the given arguments.

    Since this method is used for testing, it will create default
    values to pass to the instance.
    """

    user = kwargs.pop('user', None)
    thread = kwargs.pop('thread', None)
    body = kwargs.pop('body', 'test body')
    time_created = kwargs.pop('time_created', None)

    if len(kwargs) > 0:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    if user is None:
        user = get_user_model().objects.create_user(
            username='test',
            password='test')

    if thread is None:
        thread = create_thread()

    message_kwargs = dict(
        user=user,
        thread=thread,
        body=body)

    # Since this field has a default value defined in the model itself,
    # don't pass it if its value is None
    if time_created is not None:
        message_kwargs['time_created'] = time_created

    return models.Message.objects.create(**message_kwargs)


def create_thread(**kwargs):
    """ Create a thread instance for testing.

    Fills in default values for testing purposes.
    """

    title = kwargs.pop('title', 'test thread')
    time_created = kwargs.pop('time_created', None)

    if len(kwargs) > 0:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    thread_kwargs = dict(
        title=title)

    # Since this field has a default value defined in the model itself,
    # don't pass it if its value is None
    if time_created is not None:
        thread_kwargs['time_created'] = time_created

    return models.Thread.objects.create(**thread_kwargs)


def create_topic(**kwargs):
    """ Create topic instance for testing.

    Fills in default values for testing purposes.
    """

    title = kwargs.pop('title', 'test topic')
    description = kwargs.pop('description', 'test description')

    if len(kwargs) > 0:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    topic_kwargs = dict(
        title=title,
        description=description)

    return models.Topic.objects.create(**topic_kwargs)
