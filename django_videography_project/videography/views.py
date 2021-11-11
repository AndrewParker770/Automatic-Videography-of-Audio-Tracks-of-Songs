from django.shortcuts import render
from django.shortcuts import redirect

from Source.audioStripper import *
from Source.getLyrics import extractLyrics

from Source.firebase import sendToDatabase

from .forms import LinkForm
from .forms import FeedbackForm

import moviepy.editor as mpy
import gizeh
from bing_image_downloader import downloader

def make_frame(t):
    surface = gizeh.Surface(128,128) # width, height
    circle = gizeh.circle(32, xy = (64,64), fill=(1,1,1))
    circle.draw(surface)
    return surface.get_npimage() # returns a 8-bit RGB array

def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            deleteFiles(['Source/AudioFiles', 'Source/TextFiles'])

            audio_result = stripAudio(form.cleaned_data['youtube_link'])
            youtubeID = getID(form.cleaned_data['youtube_link'])
            text_result = extractLyrics(form.cleaned_data['artist_name'], form.cleaned_data['song_name'], youtubeID)

            downloader.download(form.cleaned_data['search_term'], limit=5,  output_dir='videography/static/imgs/', adult_filter_off=False, force_replace=False, timeout=60, verbose=True)
            
            songLength = getSongLength(youtubeID)
            audio = mpy.AudioFileClip("Source/AudioFiles/%s.wav"%(youtubeID))
            clip = mpy.VideoClip(make_frame, duration=songLength)
            clip.audio = audio
            clip.set_duration(songLength).write_videofile("videography/static/videos/%s.mp4"%(youtubeID), fps=24)

            form = LinkForm()
            context_dict = {'currentpage': 'Index', 'form': form }
            return redirect('/videography/video/%s'%(youtubeID))
    else:
        form = LinkForm()
        context_dict = {'currentpage': 'Index', 'form': form}
        return render(request, 'videography/index.html', context=context_dict)


def about(request):
    context_dict = {'currentpage': 'About'}
    return render(request, 'videography/about.html', context=context_dict)

def video(request, pk):
    video_file_path = 'videos/' + str(pk) + '.mp4'
    context_dict = {'currentpage': 'Video', 'video_file_path': video_file_path}
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