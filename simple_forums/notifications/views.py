from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from simple_forums import models as forum_models
from simple_forums.mixins import LoginRequiredMixin
from simple_forums.notifications import models
from simple_forums.utils import thread_detail_url


class ThreadNotificationCreate(LoginRequiredMixin, View):

    raise_exception = True
    required_fields = ['follow']

    def _check_required_fields(self):
        """ Make sure all required fields are present """
        for field in self.required_fields:
            if field not in self.request.POST:
                raise ValueError(
                    "The '%s' field is required." % field)

    def _follow_thread(self, user, thread):
        """ Create thread notification if it doesn't exist """
        duplicate = models.ThreadNotification.objects.filter(
            user=user, thread=thread).exists()

        if not duplicate:
            models.ThreadNotification.objects.create(user=user, thread=thread)

    def _unfollow_thread(self, user, thread):
        """ Delete notifications for the given user and thread """
        models.ThreadNotification.objects.filter(
            user=user, thread=thread).delete()

    def post(self, request, *args, **kwargs):
        """ Create a new thread notification """
        self.request = request
        self.args = args
        self.kwargs = kwargs

        try:
            self._check_required_fields()
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        follow = self.request.POST.get('follow').lower()

        if follow not in ['true', 'false']:
            return HttpResponseBadRequest(
                "'follow' must be either 'true' or 'false'")

        pk = kwargs.get('pk')
        thread = get_object_or_404(forum_models.Thread, pk=pk)

        if follow == 'true':
            self._follow_thread(request.user, thread)
        else:
            self._unfollow_thread(request.user, thread)

        redirect_url = thread_detail_url(thread=thread)

        return HttpResponseRedirect(redirect_url)
