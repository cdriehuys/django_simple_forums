from django.contrib.auth import get_user_model
from django.utils import timezone

import factory


class MessageFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating messages.
    """
    body = 'Test message body.'
    thread = factory.SubFactory('simple_forums.testing_utils.ThreadFactory')
    time_created = factory.LazyFunction(timezone.now)
    user = factory.SubFactory('simple_forums.testing_utils.UserFactory')

    class Meta:
        model = 'simple_forums.Message'


class ThreadFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating threads.
    """
    sticky = False
    time_created = factory.LazyFunction(timezone.now)
    title = factory.Sequence(lambda n: "Thread {n}".format(n=n))
    topic = factory.SubFactory('simple_forums.testing_utils.TopicFactory')

    class Meta:
        model = 'simple_forums.Thread'


class TopicFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating topics.
    """
    description = 'Test topic body.'
    title = factory.Sequence(lambda n: "Topic {n}".format(n=n))

    class Meta:
        model = 'simple_forums.Topic'


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating users.
    """
    email = factory.LazyAttribute(lambda obj: '{usr}@example.com'.format(
        usr=obj.username))
    password = 'password'
    username = factory.Sequence(lambda n: 'user{n}'.format(n=n))

    class Meta:
        django_get_or_create = ('username',)
        model = get_user_model()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default ``_create`` with our custom call.
        """
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)


def create_message(*args, **kwargs):
    return MessageFactory(*args, **kwargs)


def create_thread(*args, **kwargs):
    return ThreadFactory(*args, **kwargs)


def create_topic(*args, **kwargs):
    return TopicFactory(*args, **kwargs)


def get_test_user(*args, **kwargs):
    return UserFactory(*args, **kwargs)
