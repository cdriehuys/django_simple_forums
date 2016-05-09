from simple_forums.backends.renderers import BaseRenderer


class TextRenderer(BaseRenderer):
    """ Renders text as itself """

    def render(self, text):
        """ Return the text """
        return text
