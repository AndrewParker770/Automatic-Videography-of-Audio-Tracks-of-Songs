from django.shortcuts import render
from django.shortcuts import redirect

from Source.audioStripper import *
from Source.getLyrics import extractLyrics
from Source.captionExtractor import getKeywords
from Source.imageSearch import performImageSearch

from Source.firebase import sendToDatabase

from .forms import LinkForm
from .forms import ArtistForm
from .forms import FeedbackForm

import moviepy.editor as mpy
import gizeh
import time
import re


def make_frame(t):
    surface = gizeh.Surface(128,128) # width, height
    circle = gizeh.circle(32, xy = (64,64), fill=(1,1,1))
    circle.draw(surface)
    return surface.get_npimage() # returns a 8-bit RGB array

def index(request):
    if request.method == 'POST':

        #determine which form was submitted
        method = request.POST['operation']
        if (method == 'captions' or method == 'spoken'):
            form = LinkForm(request.POST)
            form_type = 'link'
        elif(method == 'lyrics' or method == 'music'):
            form = ArtistForm(request.POST) 
            form_type = 'artist'
        else:
            # form not of recognised type - should not be possible
            link_form = LinkForm()
            artist_form = ArtistForm()
            context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'Form was not recognised'}
            return render(request, 'videography/index.html', context=context_dict)
        
        if form.is_valid():
            deleteFiles(['Source/AudioFiles', 'Source/TextFiles', 'Source/VideoFiles', 'videography/static/imgs', 'videography/static/videos'])

            # get youtube url
            if form_type == 'artist':
                youtubeUrl = form.cleaned_data['artist_youtube_link']
            elif form_type == 'link':
                youtubeUrl = form.cleaned_data['link_youtube_link']
            
            method = request.POST['operaion']
            
            # validate url
            YOUTUBE_GENERIC = 'https://www.youtube.com/watch?v='
            index = youtubeUrl.find(YOUTUBE_GENERIC)
            if index == -1:
                #url not in https style
                link_form = LinkForm()
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'YouTube Link wrong. E.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                return render(request, 'videography/index.html', context=context_dict)
            elif index > 0:
                #does not begin with https
                link_form = LinkForm()
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'YouTube Link wrong. E.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                return render(request, 'videography/index.html', context=context_dict)
        
            

            audio_result, youtube_author = stripAudio()
            youtubeID = getID(form.cleaned_data['youtube_link'])
            
            if form.cleaned_data['caption_bool'] == "on":
                useCaptions = True
            else:
                useCaptions = False
            
            if not useCaptions:
                text_result = extractLyrics(form.cleaned_data['artist_name'], form.cleaned_data['song_name'], youtubeID)
            
            keywords = getKeywords(youtubeID, useCaptions)
            performImageSearch(keywords)
            
            songLength = getSongLength(youtubeID)

            audio = mpy.AudioFileClip("Source/AudioFiles/%s.wav"%(youtubeID))
            clip = mpy.VideoClip(make_frame, duration=songLength)
            clip.audio = audio
            clip.set_duration(songLength).write_videofile("videography/static/videos/%s.mp4"%(youtubeID), fps=24)

            return redirect('/videography/video/%s'%(youtubeID))
    else:
        link_form = LinkForm()
        artist_form = ArtistForm()
        context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form}
        return render(request, 'videography/index.html', context=context_dict)


def about(request):
    context_dict = {'currentpage': 'About'}
    return render(request, 'videography/about.html', context=context_dict)

def video(request, pk):
    video_file_path = 'videos/' + str(pk) + '.mp4'
    img_file_path = 'imgs/' + request.session['search_term'] + '/Image_1.jpg'
    context_dict = {'currentpage': 'Video', 'video_file_path': video_file_path, 'img_file_path': img_file_path}
    return render(request, 'videography/video.html', context=context_dict)

def collection(request):
    context_dict = {'currentpage': 'Collection'}
    return render(request, 'videography/collection.html', context=context_dict)

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            sendToDatabase(form.cleaned_data)
            context_dict = {'currentpage': 'Feedback'}
            return render(request, 'videography/feedback.html', context=context_dict)
    else:
        form = FeedbackForm()
        context_dict = {'currentpage': 'Feedback', 'form': form}
        return render(request, 'videography/feedback.html', context=context_dict)