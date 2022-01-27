from lyricsgenius import Genius
import sys
import os
import re

#access token - should be secure to have available
ACCESS_TOKEN = "aqMxsR0rc6Uz9WCDm0WPyqRBuHrSSgyuEVYDadc75f7bkeke83GBJRZaFyN7_W5T"

def extractLyrics(artist_name, song_name, youtubeID):
    genius = Genius(ACCESS_TOKEN)

    # won't print on terminal and won't add section titles in lyrics (e.g. [Lyrics])
    genius.verbose = False
    genius.remove_section_headers = True

    # fetch artist data, then song, then lyrics
    artist = genius.search_artist(artist_name, max_songs=1, sort="title", include_features=True)
    song = artist.song(song_name)
    lyrics = song.lyrics

    lyrics = lyrics[lyrics.find('\n'):]

    # check for then remove footer section added by genius (sometimes)
    lyrics = re.sub(r"[0-9]{2}EmbedShare URLCopyEmbedCopy", "",lyrics)

    # add lyrics into text file for later use
    with open(f"Source/TextFiles/{youtubeID}.txt", "w") as file:
        file.write(lyrics) 
    
    return os.path.exists(f"Source/TextFiles/{youtubeID}.txt")




    