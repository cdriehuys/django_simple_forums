=========
Templates
=========

All of the following templates can be overriden by a template in the ``templates/simple_forums`` directory.

base.html
  This is the base template for all the other templates. It defines the general layout of each page and contains the navigation.

login.html
  This template is used if the default login view is used, which is really the default login view from Django's authentication system.

  Context:
    - ``form``: The login form itself.
    - ``next``: The url to redirect to after a successful login. Example usage::
        
        <input type="hidden" name="next" value="{{ next }}" />

search.html
  Used for the search view. It contains a search form and an area for displaying search results.

  Context:
    - ``query``: The query string being searched for. This is only set if the query string is not blank.
    - ``results``: Contains all of the objects that matched the query. These objects may be instances of the ``Thread`` or ``Message`` models.

thread_create.html
  Used in the view for creating new threads.

  Context:
    - ``form``: The form for thread creation.

thread_detail.html
  Template used when displaying a thread and all of its replies. This template is also responsible for showing the reply form.

  Context:
    - ``reply_form``: The form used to reply to the current thread.
    - ``thread``: The current thread.

thread_list.html
  Used to show the list of threads for a topic.

  Context:
    - ``thread_list``: A list of all the non-sticky threads in the topic.
    - ``topic``: The topic whose threads are being listed.
    - ``sort_current``: The name of the current sort option.
    - ``sort_options``: A list of all possible sorting options.
    - ``sort_reversed``: True if the current sorting order is reversed, False otherwise.
    - ``sticky_thread_list``: A list of all the sticky threads in the topic.

topic_list.html
  Used to list the topics in the forum.

  Context:
    - ``topic_list``: A list of all the topics in the forum.