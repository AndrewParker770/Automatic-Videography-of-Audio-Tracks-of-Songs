import youtube_dl
import sys
import helperFunctions

def stripAudio(youtubeLink):
    youTubeID = helperFunctions.getID(youtubeLink)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'AudioFiles/{fname}.%(ext)s'.format(fname=youTubeID),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtubeLink])

if __name__ == "__main__":
    youtubeLink = sys.argv[1]
    stripAudio(youtubeLink)
    

