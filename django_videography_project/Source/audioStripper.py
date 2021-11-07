import youtube_dl
import sys

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
            ydl.download([YOUTUBE_GENERIC + youTubeID])
        result = 'Success'
    except:
        result = 'Failed'

    return result
    

if __name__ == "__main__":
    youtubeLink = sys.argv[1]
    #print(getID(youtubeLink))
    #stripAudio(youtubeLink)
    

