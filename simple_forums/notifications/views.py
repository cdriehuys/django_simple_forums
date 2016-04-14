from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from simple_forums import models as forum_models
from simple_forums.mixins import LoginRequiredMixin
from simple_forums.notifications import models
from simple_forums.utils import thread_detail_url


class ThreadNotificationCreate(LoginRequiredMixin, View):

    raise_exception = True

    def _follow_thread(self, user, thread):
        """ Create thread notification if it doesn't exist """
        duplicate = models.ThreadNotification.objects.filter(
            user=user, thread=thread).exists()

        if not duplicate:
            models.ThreadNotification.objects.create(user=user, thread=thread)
            messages.success(
                self.request, "You are now following '%s'" % thread)
        else:
            messages.warning(
                self.request, "You are already following '%s'" % thread)

    def _unfollow_thread(self, user, thread):
        """ Delete notifications for the given user and thread """
        qs = models.ThreadNotification.objects.filter(
            user=user, thread=thread)

        if qs.exists():
            qs.delete()
            messages.success(
                self.request, "You are no longer following '%s'" % thread)

    def post(self, request, *args, **kwargs):
        """ Create a new thread notification """
        self.request = request

        follow = self.request.POST.get('follow', None)

        pk = kwargs.get('pk')
        thread = get_object_or_404(forum_models.Thread, pk=pk)

        if follow:
            self._follow_thread(request.user, thread)
        else:
            self._unfollow_thread(request.user, thread)

        redirect_url = thread_detail_url(thread=thread)

        return HttpResponseRedirect(redirect_url)
