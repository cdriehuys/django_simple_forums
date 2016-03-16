from django.core.exceptions import ImproperlyConfigured

from simple_forums.utils import get_setting


class BaseSearch(object):

    # Sub-classes should override this with the settings required for
    # their search adapter connection. (host, port, password, etc.)
    REQUIRED_SETTINGS = []

    def __init__(self):
        """ Pull connection information from settings file """
        self.get_config()

    def add(self, object):
        """ Add the specified object to the search index.

        This must be implemented by the search backends that are sub-
        classes of this class.
        """
        raise NotImplementedError

    def get_config(self):
        """ Get configuration options from the settings file """
        self.connection_info = {}
        self.connection_settings = get_setting('search_backend', default={})

        for field in self.REQUIRED_SETTINGS:
            try:
                self.connection_info[field] = self.connection_settings[field]
            except KeyError:
                raise ImproperlyConfigured(
                    "Could not find '%s' in 'search_backend' setting" % field)

    def remove(self, object):
        """ Remove the specified object from the search index.

        This must be implemented by the search backends that are sub-
        classes of this class.
        """
        raise NotImplementedError

    def search(self, search_query):
        """ Search for the specified search query.

        This must be implemented by the search backends that are sub-
        classes of this class.
        """
        raise NotImplementedError

    def wipe(self):
        """ Wipes the search index.

        This must be implemented by the search backends that are sub-
        classes of this class.
        """
        raise NotImplementedError
