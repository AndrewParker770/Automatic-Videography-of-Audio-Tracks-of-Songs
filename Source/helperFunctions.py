import sys

def getID(youtubeLink):
    index = youtubeLink.find('=')
    videoID = youtubeLink[index+1:]
    return videoID