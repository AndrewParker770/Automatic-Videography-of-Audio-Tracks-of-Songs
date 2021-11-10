import getLyrics
import audioStripper

import sys
import pyfoal

if __name__ == "__main__":
    artist_name = sys.argv[1]
    song_name = sys.argv[2]
    youtubeLink = sys.argv[3]

    youtubeID = audioStripper.getID(youtubeLink)

    #audioStripper.stripAudio(youtubeLink)
    #getLyrics.extractLyrics(artist_name, song_name, youtubeID)

    alignment = pyfoal.from_file("Source/TextFiles/%s.txt" % (youtubeID), "Source/AudioFiles/%s.wav" % (youtubeID))
    print(alignment)

