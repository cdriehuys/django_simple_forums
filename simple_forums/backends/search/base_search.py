class BaseSearch(object):

    def add(self, object):
        """ Add the specified object to the search index.

        This must be implemented by the search backends that are sub-
        classes of this class.
        """
        raise NotImplementedError

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
