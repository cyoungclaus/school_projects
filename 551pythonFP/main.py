import const
import tkinter as tk
from tkinter import *
from const import root, frame, onClick
from settings import getLikedSongs, getPlaylists

#############################################################
#   Spotify Analyzer / Game Project
#   AA!-551 Final Project
#   15 May 2022
#
#   Sidenote: I have learned that tkinter is terrible
#############################################################

yButtons = 100

def build():
    getLikedSongs()
    getPlaylists()

# First Function - Lyrics Generator
button1 = tk.Button(
    master=frame,
    text="Game:\nGet Random Song Lyrics",
    command=lambda: onClick(frame, const.getLyrics()),
    bg="gray",
    fg="black",
)
button1.place(x=100, y=yButtons)

# Second Function - Playlist Randomizer
button2 = tk.Button(
    master=frame,
    text="Game:\nSong/Playlist Guesser",
    command=lambda: onClick(frame, const.playlists()),
    bg="gray",
    fg="black",
)
button2.place(x=300, y=yButtons)

# Third Function - Song Vizualizer
button3 = tk.Button(
    master=frame,
    text="3: Song",
    command=lambda: onClick(frame, const.analysis()),
    bg="gray",
    fg="black",
)
button3.place(x=500,y=yButtons)

button4 = tk.Button(
    master=frame,
    text="Rebuild Database",
    command=lambda: build(),
    bg="gray",
    fg="black",
)
button4.place(x=700,y=yButtons)


root.mainloop()
