class BaseRenderer:
    """ Base class that all renderers are based on """

    def render(self, text):
        """ Render marked up text as html """
        raise NotImplementedError
