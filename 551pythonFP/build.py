import const as c
import random
from settings import CLIENT_ID, CLIENT_SECRET, CLIENT_NAME, LIKED_SONGS, PLAYLISTS, genius

# This file will hold the functions for the buttons


def lyrics(frame):
    f = open(LIKED_SONGS).read().splitlines()
    choice = random.choice(f)
    title = str(choice.split(';')[1]).strip()
    artist = str(choice.split(';')[2]).strip()
    try:
        genius.search_song(title=title, artist=artist)
    except:
        print("Error")
        lyrics()
    print("Your song is: " + title + " by " + artist)
    c.getLyrics(frame, title, artist)
