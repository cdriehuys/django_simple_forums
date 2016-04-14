from simple_forums.notifications import models

from simple_forums.tests.testing_utils import create_thread, get_test_user


def create_thread_notification(**kwargs):
    """ Create a ThreadNotification instance for testing.

    Fills in default values for testing purposes.
    """

    user = kwargs.pop('user', get_test_user())
    thread = kwargs.pop('thread', create_thread())

    if len(kwargs):
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    notification_kwargs = dict(
        user=user,
        thread=thread)

    return models.ThreadNotification.objects.create(**notification_kwargs)
