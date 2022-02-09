from django.shortcuts import render
from django.shortcuts import redirect

from Source.audioStripper import *
from Source.getLyrics import extractLyrics

from Source.captionExtractor import getCaptions
from Source.captionExtractor import getKeywords
from Source.captionExtractor import getLyricTranscript

from Source.imageSearch import performImageSearch
from Source.imageSearch import getGoogleImage
from Source.imageSearch import extractFrames

from Source.compClip import getTimings
from Source.compClip import compileTimings
from Source.compClip import getLyricTimings

from Source.musicAlign import downloadDriver
from Source.musicAlign import getSeleniumAlign
from Source.musicAlign import validateJson
from Source.musicAlign import trimTimings

from Source.firebase import sendToDatabase
from Source.firebase import initialiseSDK

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
            
        form = ArtistForm(request.POST) 
        form_type = 'artist'
        
        if form.is_valid():
            createStaticFiles()
            deleteFiles(['Source/AudioFiles', 'Source/TextFiles', 'Source/VideoFiles', 'videography/static/imgs', 'videography/static/videos', 'Source/FrameFiles'])

            # get information from forms
            youtubeUrl = form.cleaned_data['youtube_link']
            songName = form.cleaned_data['song_name']
            artistName = form.cleaned_data['artist_name']
            
            # validate url
            YOUTUBE_GENERIC = 'https://www.youtube.com/watch?v='
            index = youtubeUrl.find(YOUTUBE_GENERIC)
            if index == -1:
                #url not in https style
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'YouTube Link wrong. E.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                return render(request, 'videography/index.html', context=context_dict)
            elif index > 0:
                #does not begin with https
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'YouTube Link wrong. E.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                return render(request, 'videography/index.html', context=context_dict)
        

            # for ease of creating files to be kept for the collection tab
            COLLECT_JSON = True

            # Generate video file
            strip_success, aliasYoutubeID = stripAudio(youtubeUrl, method) # need to generate an alias id as packages error with punctuation common in youTube ids
            if not strip_success[0] and strip_success[1] == 'Video':
                # This is a failure as lyrics require video so return to homepage
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'The video required for this metod could not extracted. Please try again or use a different method'}
                return render(request, 'videography/index.html', context=context_dict)
            
            elif not strip_success[0] and strip_success[1] == 'Audio':
                # This is a failure as lyrics require video so return to homepage
                print(strip_success)
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Could not extract audio from YouTube video,  Please try again or use a different method'}
                return render(request, 'videography/index.html', context=context_dict)
            


            trueYoutubeID = getID(youtubeUrl)

            # fetch genius lyrics if method requires it
            if method != 'captions':
                try:
                    file_create = extractLyrics(artistName, songName, aliasYoutubeID)
                    if not file_create:
                        # file was not created
                        artist_form = ArtistForm()
                        context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Lyrics could not be fetched from Genius.com. Check artist and song values'}
                        return render(request, 'videography/index.html', context=context_dict)
                except:
                    # error occured - genius lyrics could not be found
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Lyrics could not be fetched from Genius.com. Check artist and song values'}
                    return render(request, 'videography/index.html', context=context_dict)



            if method == 'lyrics':

                # get our frames
                fps = extractFrames(aliasYoutubeID)
                
                #get key words from lyrics text file created above
                keywords = getKeywords(aliasYoutubeID)

                # get images to use in video
                getGoogleImage(keywords)

                # get a transcript from lyrics (will need to pass keywords)
                frame_list = getLyricTranscript(keywords, fps)
                timings = getLyricTimings(frame_list, fps)

                # get youtube video audio
                audioclip = VideoFileClip(f"Source/VideoFiles/{aliasYoutubeID}.mp4").audio
                song_duration = audioclip.duration

                #create video
                compileTimings(timings, song_duration, aliasYoutubeID, audioclip)

                if COLLECT_JSON: 
                    createCollectionJSON(songName, artistName, trueYoutubeID, timings, aliasYoutubeID)

                return redirect(f'/videography/video/{trueYoutubeID}')


            # 'music'
            elif method == 'music':

                #get key words from lyrics text file created above
                keywords = getKeywords(aliasYoutubeID)

                # get images to use in video
                getGoogleImage(keywords)

                #generate alignment through selenium
                print("Going In")
                getSeleniumAlign(aliasYoutubeID)
                print("Coiming Out")

                #keep getting alignment from website
                counter = 0
                while counter < 5:
                    invalid = validateJson(aliasYoutubeID)
                    if invalid:
                        getSeleniumAlign(aliasYoutubeID)
                        counter += 1
                    else:
                        break

                if counter == 5 and not validateJson(aliasYoutubeID):
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Forced alignment has failed'}
                    return render(request, 'videography/index.html', context=context_dict)
                
                # get youtube video audio
                if strip_success[1] == 'Video':
                    audioclip = VideoFileClip(f"Source/VideoFiles/{aliasYoutubeID}.mp4").audio
                elif strip_success[1] == 'Audio':
                    audioclip = AudioFileClip(f"Source/AudioFiles/{aliasYoutubeID}.mp3")
                song_duration = audioclip.duration

                timings = trimTimings(keywords, song_duration, buffer=1)
                compileTimings(timings, song_duration, aliasYoutubeID, audioclip)

                if COLLECT_JSON: 
                    createCollectionJSON(songName, artistName, trueYoutubeID, timings, aliasYoutubeID)

                return redirect(f'/videography/video/{trueYoutubeID}')


            elif method == 'captions':
                success, transcript_dict = getCaptions(trueYoutubeID, aliasYoutubeID)
                keywords = getKeywords(aliasYoutubeID)

                # get images to use in video
                getGoogleImage(keywords)

                # get youtube video audio
                if strip_success[1] == 'Video':
                    audioclip = VideoFileClip(f"Source/VideoFiles/{aliasYoutubeID}.mp4").audio
                elif strip_success[1] == 'Audio':
                    audioclip = AudioFileClip(f"Source/AudioFiles/{aliasYoutubeID}.mp3")
                song_duration = audioclip.duration

                #create video
                #TODO: make a better estimation of where the words are
                timings = getTimings(keywords, transcript_dict)
                compileTimings(timings, song_duration, aliasYoutubeID, audioclip)

                if COLLECT_JSON: 
                    createCollectionJSON(songName, artistName, trueYoutubeID, timings, aliasYoutubeID)

                return redirect(f'/videography/video/{trueYoutubeID}')

    else:
        # This is the GET request for the page
        artist_form = ArtistForm()
        context_dict = {'currentpage': 'Index', 'artist_form':artist_form}
        return render(request, 'videography/index.html', context=context_dict)


def about(request):
    context_dict = {'currentpage': 'About'}
    return render(request, 'videography/about.html', context=context_dict)

def video(request, pk):
    file_name = re.sub('[^a-zA-Z1-9]', '0', str(pk))

    video_file_path = f'videos/{file_name}.mp4'

    if not os.path.exists(os.path.join(os.getcwd(), "videography", "static", video_file_path)):
        if os.path.exists(os.path.join(os.getcwd(), "videography", "static", f'collection/{file_name}.mp4')):
            video_file_path = f'collection/{file_name}.mp4'
        else:
            video_file_path = None
    

    context_dict = {'currentpage': 'Video', 'video_file_path': video_file_path}
    return render(request, 'videography/video.html', context=context_dict)

def collection(request):
    context_dict = {'currentpage': 'Collection'}

    json_files = []
    path = os.path.join(os.getcwd(), 'videography', 'static', 'collection')
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open (os.path.join(path, file), 'r') as f:
                entry = json.load(f)
                json_files.append(entry)
    
    context_dict['files'] = json_files

    return render(request, 'videography/collection.html', context=context_dict)

def feedback(request):
    SDK_FOUND, sdk_path = initialiseSDK()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            sendToDatabase(form.cleaned_data)
            artist_form = ArtistForm()
            context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'message': "Submittion complete. Thank you for providing feedback."}
            return render(request, 'videography/index.html', context=context_dict)
    else:
        form = FeedbackForm()
        context_dict = {'currentpage': 'Feedback', 'form': form, 'found': SDK_FOUND}
        return render(request, 'videography/feedback.html', context=context_dict)