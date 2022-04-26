import const as c
import random
from settings import CLIENT_ID, CLIENT_SECRET, CLIENT_NAME, LIKED_SONGS, PLAYLISTS

# This file will hold the functions for the buttons


def lyrics(frame):
    f = open(LIKED_SONGS).read().splitlines()
    choice = random.choice(f)
    name = str(choice.split(';')[1]).strip()
    artist = str(choice.split(';')[2]).strip()
    try:
        print("Your song is: " + name + " by " + artist)
    except:
        lyrics()
    c.getLyrics(frame, name, artist)
