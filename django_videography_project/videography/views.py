from django.shortcuts import render
from django.shortcuts import redirect

from Source.audioStripper import *
from Source.getLyrics import extractLyrics

from Source.captionExtractor import getCaptions
from Source.captionExtractor import getKeywords

from Source.imageSearch import performImageSearch
from Source.imageSearch import getGoogleImage

from Source.compClip import getTimings
from Source.compClip import compileTimings

from Source.firebase import sendToDatabase

from .forms import LinkForm
from .forms import ArtistForm
from .forms import FeedbackForm

from moviepy.editor import *
import gizeh
import time
import re
import json



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

            # get information from forms
            if form_type == 'artist':
                youtubeUrl = form.cleaned_data['youtube_link']
                songName = form.cleaned_data['song_name']
                artistName = form.cleaned_data['artist_name']
            elif form_type == 'link':
                youtubeUrl = form.cleaned_data['youtube_link']

            """

            To be removed

            """
            if (method == 'music'): #method == 'spoken' or 
                link_form = LinkForm()
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'This option is currently not functional'}
                return render(request, 'videography/index.html', context=context_dict)
            
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
        
            
            audio_result, youtube_author = stripAudio(youtubeUrl)
            youtubeID = getID(youtubeUrl)

            # fetch genius lyrics if method requires it
            if form_type == 'artist':
                try:
                    file_create = extractLyrics(artistName, songName, youtubeID)
                    if not file_create:
                        # file was not created
                        link_form = LinkForm()
                        artist_form = ArtistForm()
                        context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'Lyrics could not be fetched from Genius.com. Check artist and song values'}
                        return render(request, 'videography/index.html', context=context_dict)
                except:
                    # error occured - genius lyrics could not be found
                    link_form = LinkForm()
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'Lyrics could not be fetched from Genius.com. Check artist and song values'}
                    return render(request, 'videography/index.html', context=context_dict)
            else:
                if method == 'captions':
                    success, transcript_dict = getCaptions(youtubeID)
                    keywords = getKeywords(youtubeID)

                    # get images to use in video
                    getGoogleImage(keywords)

                    # get youtube video audio
                    audioclip = VideoFileClip(f"Source/VideoFiles/{youtubeID}.mp4").audio
                    song_duration = audioclip.duration

                    timings = getTimings(keywords, transcript_dict, youtubeID)
                    compileTimings(timings, song_duration, youtubeID, audioclip)

                    return redirect('/videography/video/%s'%(youtubeID))


                    #with open('Source/TextFiles/json.txt', 'w') as outfile:
                    #    json.dump(transcript_dict, outfile)

                    #with open('Source/TextFiles/keys.txt', 'w') as outfile:
                    #    for word in keywords:
                    #        outfile.write(f'{word}')

                    #delete this
                    link_form = LinkForm()
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'Redirect after captions'}
                    return render(request, 'videography/index.html', context=context_dict)

                if method == 'spoken':
                    #delete this
                    link_form = LinkForm()
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'link_form': link_form,'artist_form':artist_form, 'error': 'Redirect after spoken'}
                    return render(request, 'videography/index.html', context=context_dict)
                    

                #speech recognsion 

            keywords = getKeywords(youtubeID)
            performImageSearch(keywords)
            songLength = getSongLength(youtubeID)

            

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