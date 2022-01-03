import youtube_dl
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
    youTubeID = getID(youtubeLink)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'Source/AudioFiles/{fname}.%(ext)s'.format(fname=youTubeID),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    YOUTUBE_GENERIC = 'https://www.youtube.com/watch?v='

    try:
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(YOUTUBE_GENERIC + youTubeID, download=True)
        result = 'Success'
    except:
        result = 'Failed'

    return result, meta['uploader']
    
    

