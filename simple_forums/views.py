from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from simple_forums import forms, models
from simple_forums.backends.search import get_search_class
from simple_forums.mixins import LoginRequiredMixin
from simple_forums.utils import thread_detail_url


class SearchView(generic.View):
    """ View for searching """

    template_name = 'simple_forums/search.html'
    query_kwarg = 'q'

    def get(self, request, *args, **kwargs):
        """ Show the search form and results if applicable """
        self.args = args
        self.kwargs = kwargs
        self.request = request

        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = dict()

        query = self.get_query()
        if query is not None:
            context['query'] = query
            context['results'] = self.get_queryset()

        return context

    def get_query(self):
        """ Return the query passed as a GET parameter """
        return self.request.GET.get(self.query_kwarg, None)

    def get_queryset(self):
        """ Return the list of threads that match the query """
        backend = get_search_class()()

        results = backend.search(self.get_query())

        return [result for result, _ in results]


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
            message = form.save(request.user, self.object)

            return HttpResponseRedirect(message.get_absolute_url())

        context = self.get_context_data()
        context['reply_form'] = form

        return render(request, self.get_template_names(), context)


class ThreadListView(generic.ListView):
    """ View for listing threads """

    model = models.Thread
    reverse_kwarg = 'rev'
    sort_default = 'activity'
    sort_default_reverse = True
    sort_mapping = {
        'activity': 'time_last_activity',
        'title': 'title',
    }
    sort_kwarg = 'sort'

    def get_context_data(self, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)

        context['sort_current'] = self.sort_name
        context['sort_options'] = [item for item in self.sort_mapping]
        context['sort_reversed'] = self.sort_reversed

        sticky_threads = self._get_base_queryset().filter(sticky=True)
        context['sticky_thread_list'] = sticky_threads

        topic = get_object_or_404(
            models.Topic,
            pk=self.kwargs.get('topic_pk'))
        context['topic'] = topic

        return context

    def _get_base_queryset(self):
        """ Retrieve all threads associated with the given topic """
        topic = get_object_or_404(
            models.Topic,
            pk=self.kwargs.get('topic_pk'))

        return self.model.objects.filter(topic=topic)

    def get_queryset(self):
        """ Return all non-sticky threads """
        self.sort_name = self.request.GET.get(
            self.sort_kwarg,
            None)

        if self.sort_name not in self.sort_mapping:
            self.sort_name = 'activity'
            self.sort_reversed = True
        else:
            self.sort_reversed = self.request.GET.get(
                self.reverse_kwarg, None) == 'true'

        self.sort_field = self.sort_mapping.get(self.sort_name)

        if self.sort_reversed:
            self.sort_field = '-%s' % self.sort_field

        queryset = self._get_base_queryset()
        # exclude sticky posts
        queryset = queryset.exclude(sticky=True)
        # apply sorting
        queryset = queryset.order_by(self.sort_field)

        return queryset


class TopicListView(generic.ListView):
    """ View for listing topics """

    model = models.Topic
