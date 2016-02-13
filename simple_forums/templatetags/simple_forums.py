from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode


register = template.Library()


@register.simple_tag(takes_context=True)
def login_url(context):
    """ Construct a login url that redirects to the current page. """
    request = context.get('request')
    return '%s?next=%s' % (
        reverse('login'),
        urlencode(request.path))


@register.simple_tag(takes_context=True)
def logout_url(context):
    """ Construct a logout url that redirects to the current page. """
    request = context.get('request')
    return '%s?next=%s' % (
        reverse('logout'),
        urlencode(request.path))
