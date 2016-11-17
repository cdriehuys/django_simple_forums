import pytest

from simple_forums.testing_utils import (
    MessageFactory, ThreadFactory, UserFactory)


@pytest.fixture(scope='function')
def msg_factory(db):
    """
    Return the ``MessageFactory`` class.

    Also ensures the django db is set up.

    Returns:
        ``simple_forums.testing_utils.MessageFactory``.
    """
    return MessageFactory


@pytest.fixture(scope='function')
def thread_factory(db):
    """
    Return the ``ThreadFactory`` class.

    Also ensures the django db is set up.

    Returns:
        ``simple_forums.testing_utils.ThreadFactory``
    """
    return ThreadFactory


@pytest.fixture(scope='function')
def usr_factory(db):
    """
    Return the ``UserFactory`` class.

    Also ensures the django db is set up.

    Returns:
        ``simple_forums.testing_utils.UserFactory``
    """
    return UserFactory
