from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode

from simple_forums.utils import get_setting, string_to_class


register = template.Library()


def get_renderer_class():
    """ Determine the renderer class from the settings file """
    render_string = get_setting(
        'markup_renderer',
        'simple_forums.backends.renderers.TextRenderer')

    return string_to_class(render_string)


@register.simple_tag(takes_context=True)
def login_url(context, view_name='simple-forums:login'):
    """ Construct a login url that redirects to the current page. """
    request = context.get('request')
    return '%s?next=%s' % (
        reverse(view_name),
        urlencode(request.path))


@register.simple_tag(takes_context=True)
def logout_url(context, view_name='simple-forums:logout'):
    """ Construct a logout url that redirects to the current page. """
    request = context.get('request')
    return '%s?next=%s' % (
        reverse(view_name),
        urlencode(request.path))


@register.simple_tag
def render_markup(text):
    """ Render text using the renderer specified in settings.py """
    renderer_class = get_renderer_class()
    renderer = renderer_class()

    return renderer.render(text)
