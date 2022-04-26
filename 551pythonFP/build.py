import const as c
import random
from __init__ import LIKED_SONGS, PLAYLISTS

# This file will hold the funtions for the buttons

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
