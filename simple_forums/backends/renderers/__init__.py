class BaseRenderer:
    """ Base class that all renderers are based on """

    def render(self, text):
        """ Render marked up text as html """
        raise NotImplementedError

# make renderers easily accessible
from simple_forums.backends.renderers.markdown_renderer import (			# noqa
    MarkdownRenderer)
from simple_forums.backends.renderers.text_renderer import TextRenderer  	# noqa
