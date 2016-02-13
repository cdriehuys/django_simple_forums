from django import forms

from simple_forums import models


class ThreadCreationForm(forms.Form):
    """ Form for creating new threads """
    topic = forms.ModelChoiceField(queryset=models.Topic.objects.all())
    title = forms.CharField(max_length=200)
    body = forms.CharField(label='Post Body', widget=forms.Textarea)

    def save(self, user):
        """ Save the contents of the form.

        Uses the title field to create a new thread, and uses the body
        field to create a new message associated with the created
        thread.
        """
        if self.is_valid():

            topic = self.cleaned_data['topic']

            thread = models.Thread.objects.create(
                topic=topic,
                title=self.cleaned_data['title'])

            models.Message.objects.create(
                user=user,
                thread=thread,
                body=self.cleaned_data['body'])

            return thread


class ThreadReplyForm(forms.Form):
    """ Form for replying to threads """
    body = forms.CharField(label='Reply', widget=forms.Textarea)

    def save(self, user, thread):
        """ Save the contents of the form.

        Creates a new reply on the given thread by the given user.
        """
        if self.is_valid():
            return models.Message.objects.create(
                user=user,
                thread=thread,
                body=self.cleaned_data['body'])
