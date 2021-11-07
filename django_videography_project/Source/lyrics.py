from lyricsgenius import Genius
import sys

ACCESS_TOKEN = "aqMxsR0rc6Uz9WCDm0WPyqRBuHrSSgyuEVYDadc75f7bkeke83GBJRZaFyN7_W5T"

if __name__ == "__main__":
    artist_name = sys.argv[1]

    genius = Genius(ACCESS_TOKEN)
    artist = genius.search_artist(artist_name, max_songs=3, sort="title")

    song = artist.song("")

    print(song)