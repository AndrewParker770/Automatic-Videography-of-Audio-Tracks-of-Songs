from pytube import YouTube
import moviepy.editor
import sys, os, shutil
import time
import librosa
import re
import json

import youtube_dl

def deleteFiles(folders):
    for folder in folders:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Error: Unable to delete %s.' % (file_path))

def getSongLength(youtubeID):
    y, sr = librosa.load("Source/AudioFiles/%s.wav"%(youtubeID))
    return librosa.get_duration(y=y, sr=sr)

def getID(youtubeLink):
    firstIndex = youtubeLink.find('=')
    secondIndex = youtubeLink.find('&')
    if (secondIndex == -1):
        videoID = youtubeLink[firstIndex+1:]
    else:
        videoID = youtubeLink[firstIndex+1:secondIndex]
    return videoID

def stripAudio(youtubeLink, method):
    youtubeID = getID(youtubeLink)
    fakeYoutubeID = re.sub('[^a-zA-Z1-9]', '0', youtubeID)


    try:
        yt = YouTube(youtubeLink)
        video_file_extension = 'mp4'
        filename = f"{fakeYoutubeID}.{video_file_extension}"
        yt.streams.filter(progressive=True, file_extension=video_file_extension).order_by('resolution').desc().first().download("Source/VideoFiles/", filename=filename)
        result = True

        audio_file_extension = "mp3"
        video = moviepy.editor.VideoFileClip("Source/VideoFiles/" + f"{fakeYoutubeID}.{video_file_extension}")
        audio = video.audio

        audio.write_audiofile("Source/AudioFiles/" + f"{fakeYoutubeID}.{audio_file_extension}")

        author = yt.author
        success = (True, 'Video')

    except:
        if method == 'lyrics':
            #Failure to extract video for lyrics method is a failure 
            success = (False, 'Video')
        else:
            #other methods can recover if audio only extracted
            try:
                backupAudioStripper(youtubeID)
                success = (True, 'Audio')
            except: 
                success = (False, 'Audio')
    return success, fakeYoutubeID

def backupAudioStripper(youtubeID):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'Source/AudioFiles/{youtubeID}.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtubeID])

def createCollectionJSON(song_name, artist_name, youtubeID, timings, aliasYoutubeID):
    
    json_string = {
        "song_name" : song_name,
        "artist_name" : artist_name,
        "youtubeID" : youtubeID,
        "timings": timings
    }
    
    collectionPath = os.path.join(os.getcwd(), "videography", "static", "collection")

    with open(os.path.join(collectionPath, f'{aliasYoutubeID}.json'), 'w') as f:
        json.dump(json_string, f)

    return

def createStaticFiles():
    path_to_static = os.path.join(os.getcwd(), "videography", "static")
    if not os.path.exists(path_to_static):
        os.mkdir(path_to_static)

    if not os.path.exists(os.path.join(path_to_static, "collection")):
        os.mkdir(os.path.join(path_to_static, "collection"))
    
    if not os.path.exists(os.path.join(path_to_static, "imgs")):
        os.mkdir(os.path.join(path_to_static, "imgs"))
    
    if not os.path.exists(os.path.join(path_to_static, "videos")):
        os.mkdir(os.path.join(path_to_static, "videos"))




    

