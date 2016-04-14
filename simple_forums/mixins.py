from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


class LoginRequiredMixin(object):
    """ Mixin for class based views that requires a user to log in """

    raise_exception = False

    def _handle_not_authenticated(self, request):
        if self.raise_exception:
            return HttpResponseForbidden()

        return redirect_to_login(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self._handle_not_authenticated(request)

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)
