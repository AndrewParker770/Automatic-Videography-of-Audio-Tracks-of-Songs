from pytube import YouTube
import moviepy.editor
import sys, os, shutil
import time
import librosa

def waitFor(seconds):
    time.sleep(seconds)
    return True

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

def stripAudio(youtubeLink):
    youtubeID = getID(youtubeLink)

    yt = YouTube(youtubeLink)
    video_file_extension = 'mp4'
    filename = youtubeID + "." + video_file_extension
    yt.streams.filter(progressive=True, file_extension=video_file_extension).order_by('resolution').desc().first().download("Source/VideoFiles/", filename=filename)
    result = True

    audio_file_extension = "wav"
    video = moviepy.editor.VideoFileClip("Source/VideoFiles/" + f"{youtubeID}.{video_file_extension}")
    audio = video.audio

    audio.write_audiofile("Source/AudioFiles/" + f"{youtubeID}.{audio_file_extension}")

    author = yt.author

    return result, author
    
    

