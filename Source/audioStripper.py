import youtube_dl
import sys
import helperFunctions

def getID(youtubeLink):
    index = youtubeLink.find('=')
    videoID = youtubeLink[index+1:]
    return videoID

if __name__ == "__main__":

    youtubeLink = sys.argv[1]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'AudioFiles/%s.wav'%(helperFunctions.getID(youtubeLink)),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtubeLink])

