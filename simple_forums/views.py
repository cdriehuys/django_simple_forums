from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic

from simple_forums import forms, models
from simple_forums.utils import thread_detail_url


class ThreadCreateView(LoginRequiredMixin, generic.edit.FormView):
    """ View for creating new threads """

    template_name = 'simple_forums/thread_create.html'
    form_class = forms.ThreadCreationForm

    def form_valid(self, form):
        """ Save form if it is valid """
        thread = form.save(self.request.user)

        return HttpResponseRedirect(thread_detail_url(thread=thread))


class ThreadDetailView(generic.DetailView):
    """ View for getting a thread's details """

    model = models.Thread
    pk_url_kwarg = 'thread_pk'


class ThreadListView(generic.ListView):
    """ View for listing threads """

    model = models.Thread

    def get_queryset(self):
        """ Filter the queryset based on topic.

        The only threads that should be included are the ones for the
        topic specified in the url.
        """
        topic = get_object_or_404(
            models.Topic,
            pk=self.kwargs.get('topic_pk'))

        return self.model.objects.filter(topic=topic)


class TopicListView(generic.ListView):
    """ View for listing topics """

    model = models.Topic
