from django.conf import settings
from django.test import modify_settings, RequestFactory, TestCase

from simple_forums.context_processors import installed_apps


class TestInstalledAppsContextProcessor(TestCase):

    NOTIFICATIONS_INSTALLED = {
        'append': 'simple_forums.notifications',
    }
    NOTIFICATIONS_UNINSTALLED = {
        'remove': 'simple_forums.notifications',
    }

    def setUp(self):
        self.factory = RequestFactory()

    @modify_settings(INSTALLED_APPS=NOTIFICATIONS_INSTALLED)
    def test_notifications_installed(self):
        """ Test processor when notifications is installed.

        If 'simple_forums.notifications' is in INSTALLED_APPS, then
        'notifications_installed' should be true.
        """
        request = self.factory.get('/')

        expected = {
            'installed_apps': settings.INSTALLED_APPS,
            'notifications_installed': True,
        }

        self.assertDictEqual(expected, installed_apps(request))

    @modify_settings(INSTALLED_APPS=NOTIFICATIONS_UNINSTALLED)
    def test_notifications_uninstalled(self):
        """ Test processor when notifications is not installed.

        If 'simple_forums.notifications' is not in INSTALLED_APPS, then
        'notifications_installed' should be false.
        """
        request = self.factory.get('/')

        expected = {
            'installed_apps': settings.INSTALLED_APPS,
            'notifications_installed': False,
        }

        self.assertDictEqual(expected, installed_apps(request))
