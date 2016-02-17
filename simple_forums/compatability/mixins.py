from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """ Mixin for class based views that requires a user to log in """

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
