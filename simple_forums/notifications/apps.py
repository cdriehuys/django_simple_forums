from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'simple_forums.notifications'

    def ready(self):
        import simple_forums.notifications.signals  # noqa
