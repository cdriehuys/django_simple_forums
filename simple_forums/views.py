from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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

    def get_context_data(self, **kwargs):
        context = super(ThreadDetailView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            context['reply_form'] = forms.ThreadReplyForm()

        return context

    def post(self, request, *args, **kwargs):
        """ Create a new reply to the current thread """
        if not request.user.is_authenticated():
            raise PermissionDenied()

        self.object = self.get_object()

        form = forms.ThreadReplyForm(request.POST)

        if form.is_valid():
            form.save(request.user, self.object)

            return HttpResponseRedirect(thread_detail_url(thread=self.object))

        return render(request, self.get_template_names(), {'reply_form': form})


class ThreadListView(generic.ListView):
    """ View for listing threads """

    model = models.Thread

    def get_context_data(self, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)

        sticky_threads = self._get_base_queryset().filter(sticky=True)
        context['sticky_thread_list'] = sticky_threads

        return context

    def _get_base_queryset(self):
        """ Retrieve all threads associated with the given topic """
        topic = get_object_or_404(
            models.Topic,
            pk=self.kwargs.get('topic_pk'))

        return self.model.objects.filter(topic=topic)

    def get_queryset(self):
        """ Return all non-sticky threads """
        return self._get_base_queryset() \
            .exclude(sticky=True) \
            .order_by('-time_last_activity')


class TopicListView(generic.ListView):
    """ View for listing topics """

    model = models.Topic
