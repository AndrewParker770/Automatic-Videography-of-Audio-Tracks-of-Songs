from django.shortcuts import render
from django.shortcuts import redirect

from Source.audioStripper import *
from Source.getLyrics import *
from Source.captionExtractor import *
from Source.imageSearch import *
from Source.compClip import *
from Source.musicAlign import *

from Source.firebase import *

from .forms import LinkForm
from .forms import ArtistForm
from .forms import FeedbackForm

from moviepy.editor import *
import time
import re
import json



def index(request):
    
    #IF new process begins signal to stop this one
    STOP_PROCESSING = False
    stop_name = str(time.time()).split(".")[0] + ".txt"
    static_path = os.path.join(os.getcwd(),"videography", "static")
    stop_file_path = os.path.join(static_path, stop_name)

    #delete previous stop file
    files_in_static = os.listdir(static_path)
    for text_file in [file for file in files_in_static if file.endswith(".txt")]:
        os.remove(os.path.join(static_path, text_file))

    #create the new stop file
    with open(stop_file_path, 'w'):
        pass

    if request.method == 'POST':
        #determine which form was submitted
        method = request.POST['operation']
            
        form = ArtistForm(request.POST) 
        form_type = 'artist'
        
        if form.is_valid():
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
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'YouTube Link in the wrong format. Please try again with link similar to this example: https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                return render(request, 'videography/index.html', context=context_dict)
            elif index > 0:
                #does not begin with https
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'YouTube Link in the wrong format. Please try again with link similar to this example: https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                return render(request, 'videography/index.html', context=context_dict)
        

            # for ease of creating files to be kept for the collection tab
            COLLECT_JSON = True

            # Generate video file
            print("Begin strip")
            strip_success, aliasYoutubeID = stripAudio(youtubeUrl, method) # need to generate an alias id as packages error with punctuation common in youTube ids
            if not strip_success[0] and strip_success[1] == 'Video':
                # This is a failure as lyrics require video so return to homepage
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'The video required for this method could not extracted. Please try again or use a different method'}
                return render(request, 'videography/index.html', context=context_dict)
            
            elif not strip_success[0] and strip_success[1] == 'Audio':
                # This is a failure as lyrics require video so return to homepage
                artist_form = ArtistForm()
                context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Could not extract audio from YouTube video. Please try again or use a different method'}
                return render(request, 'videography/index.html', context=context_dict)
            
            print("Strip successful")


            trueYoutubeID = getID(youtubeUrl)

            print("Getting Lyrics!")
            # fetch genius lyrics if method requires it
            if method != 'captions':
                try:
                    file_create = extractLyrics(artistName, songName, aliasYoutubeID)
                    if not file_create:
                        # file was not created
                        artist_form = ArtistForm()
                        context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Lyrics could not be fetched from Genius.com. Check artist and song values are correct and try again.'}
                        return render(request, 'videography/index.html', context=context_dict)
                except:
                    # error occured - genius lyrics could not be found
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Lyrics could not be fetched from Genius.com. Check artist and song values are correct and try again.'}
                    return render(request, 'videography/index.html', context=context_dict)

            print("Received Lyrics")


            if method == 'lyrics':

                # get our frames
                fps = extractFrames(aliasYoutubeID)
                
                #get key words from lyrics text file created above
                keywords = getKeywords(aliasYoutubeID)

                # get images to use in video
                for word in keywords:
                    #used to interupt processes
                    if os.path.exists(stop_file_path):
                        getGoogleImage(word)
                    else:
                        STOP_PROCESSING = True
                        break

                if not STOP_PROCESSING:
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
                else:
                    # don't return anything as processing not completed
                    pass


            # 'music'
            elif method == 'music':

                #get key words from lyrics text file created above
                keywords = getKeywords(aliasYoutubeID)

                #generate alignment through selenium
                success = getSeleniumAlign(aliasYoutubeID)
                if not success:
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Selenium driver could not initalise. Check that Chrome on user device is up-to-date'}
                    return render(request, 'videography/index.html', context=context_dict)
                
                
                if validateJson(aliasYoutubeID):
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Forced alignment values have failed to be fecthed. Please try again.'}
                    return render(request, 'videography/index.html', context=context_dict)
                
                # get images to use in video
                for word in keywords:
                    #used to interupt processes
                    if os.path.exists(stop_file_path):
                        getGoogleImage(word)
                    else:
                        STOP_PROCESSING = True
                        break

                if not STOP_PROCESSING:
                    # get youtube video audio
                    if strip_success[1] == 'Video':
                        audioclip = VideoFileClip(f"Source/VideoFiles/{aliasYoutubeID}.mp4").audio
                    elif strip_success[1] == 'Audio':
                        audioclip = AudioFileClip(f"Source/AudioFiles/{aliasYoutubeID}.mp3")
                    song_duration = audioclip.duration

                    if os.path.exists(stop_file_path):
                        timings = trimTimings(keywords, song_duration, buffer=1)
                        compileTimings(timings, song_duration, aliasYoutubeID, audioclip)

                        if COLLECT_JSON: 
                            createCollectionJSON(songName, artistName, trueYoutubeID, timings, aliasYoutubeID)

                        return redirect(f'/videography/video/{trueYoutubeID}')
                    else:
                        # don't return anything as processing not completed
                        pass 
                else: 
                    # don't return anything as processing not completed
                    pass

            elif method == 'captions':
                success, transcript_dict = getCaptions(trueYoutubeID, aliasYoutubeID)
                if not success:
                    artist_form = ArtistForm()
                    context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'error': 'Captions could not be extracted. Check that referenced YouTube video has captions and try again.'}
                    return render(request, 'videography/index.html', context=context_dict)


                keywords = getKeywords(aliasYoutubeID)

                # get images to use in video
                for word in keywords:
                    #used to interupt processes
                    if os.path.exists(stop_file_path):
                        getGoogleImage(word)
                    else:
                        STOP_PROCESSING = True
                        break

                if not STOP_PROCESSING:

                    # get youtube video audio
                    if strip_success[1] == 'Video':
                        audioclip = VideoFileClip(f"Source/VideoFiles/{aliasYoutubeID}.mp4").audio
                    elif strip_success[1] == 'Audio':
                        audioclip = AudioFileClip(f"Source/AudioFiles/{aliasYoutubeID}.mp3")
                    song_duration = audioclip.duration

                    #create video
                    timings = getTimings(keywords, transcript_dict)
                    compileTimings(timings, song_duration, aliasYoutubeID, audioclip)

                    if COLLECT_JSON: 
                        createCollectionJSON(songName, artistName, trueYoutubeID, timings, aliasYoutubeID)

                    return redirect(f'/videography/video/{trueYoutubeID}')
                else:
                    # don't return anything as processing not completed
                    pass
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
            CURRENT_PAGE = "Index"
            context_dict = {'currentpage': 'Index', 'artist_form':artist_form, 'message': "Submittion complete. Thank you for providing feedback."}
            return render(request, 'videography/index.html', context=context_dict)
    else:
        form = FeedbackForm()
        CURRENT_PAGE = "Feedback"
        context_dict = {'currentpage': 'Feedback', 'form': form, 'found': SDK_FOUND}
        return render(request, 'videography/feedback.html', context=context_dict)