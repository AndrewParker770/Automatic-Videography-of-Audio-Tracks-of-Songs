from django import forms

CHOICES = [('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5')]

class ArtistForm(forms.Form):
    artist_youtube_link = forms.CharField(label='YouTube Link:', max_length=100, widget=forms.TextInput(attrs={'rows':1, 'class': 'form-control'}))
    artist_name = forms.CharField(label='Artist Name:', max_length=100, widget=forms.TextInput(attrs={'rows':1, 'class': 'form-control'}))
    song_name = forms.CharField(label='Song Name:', max_length=100, widget=forms.TextInput(attrs={'rows':1, 'class': 'form-control'}))

class LinkForm(forms.Form):
    link_youtube_link = forms.CharField(label='YouTube Link:', max_length=100, widget=forms.TextInput(attrs={'rows':1, 'class': 'form-control'}))

class FeedbackForm(forms.Form):
    first_name = forms.CharField(label='First Name:', max_length=100, widget=forms.TextInput(attrs={'rows':1, 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name:', max_length=100, widget=forms.TextInput(attrs={'rows':1, 'class': 'form-control'}))
    preference_ranking = forms.CharField(label='How good is the video?', widget=forms.Select(choices=CHOICES, attrs={'class': 'form-control'}))

    