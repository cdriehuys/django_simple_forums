import bleach

from bleach_whitelist.bleach_whitelist import markdown_attrs, markdown_tags

from django.conf import settings

from markdown import markdown


class BaseRenderer:
    """ Base class that all renderers are based on """

    def render(self, text):
        """ Render marked up text as html """
        raise NotImplementedError


class MarkdownRenderer(BaseRenderer):
    """ Handles rendering markdown into html """

    DEFAULT_EXTENSIONS = [
        'pymdownx.github',
    ]

    @staticmethod
    def get_extensions():
        """ Get a list of extensions to use """
        return settings.SIMPLE_FORUMS.get(
            'markdown_extensions',
            MarkdownRenderer.DEFAULT_EXTENSIONS)

    def render(self, text):
        """ Convert the given text into html """
        converted = markdown(
            text,
            extensions=MarkdownRenderer.get_extensions())

        return bleach.clean(
            converted,
            tags=markdown_tags + ['pre'],
            attributes=markdown_attrs)
