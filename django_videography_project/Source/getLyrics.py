from lyricsgenius import Genius
import sys

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

    # check for then remove footer section added by genius (sometimes)
    char = lyrics.find('98EmbedShare URLCopyEmbedCopy')
    if (char != -1):
        lyrics = lyrics[:char]

    # add lyrics into text file for later use
    with open("Source/TextFiles/%s.txt" % (youtubeID), "w") as file:
        file.write(lyrics) 


if __name__ == "__main__":
    artist_name = sys.argv[1]
    song_name = sys.argv[2]
    youtubeID = sys.argv[3]

    extractLyrics(artist_name, song_name, youtubeID)




    