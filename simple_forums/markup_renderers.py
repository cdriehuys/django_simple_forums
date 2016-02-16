import bleach

from bleach_whitelist.bleach_whitelist import markdown_attrs, markdown_tags

from markdown import markdown


class BaseRenderer:
    """ Base class that all renderers are based on """

    def render(self, text):
        """ Render marked up text as html """
        raise NotImplementedError


class MarkdownRenderer(BaseRenderer):
    """ Handles rendering markdown into html """

    def render(self, text):
        """ Convert the given text into html """
        converted = markdown(text)

        return bleach.clean(
            converted,
            tags=markdown_tags,
            attributes=markdown_attrs)
