from django import forms


class ThreadCreationForm(forms.Form):
    """ Form for creating new threads """

    title = forms.CharField(max_length=200)
    body = forms.CharField(label='Post Body', widget=forms.Textarea)
