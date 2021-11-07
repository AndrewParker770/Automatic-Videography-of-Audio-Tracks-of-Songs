from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(label='YouTube Hyperlink:', max_length=100)