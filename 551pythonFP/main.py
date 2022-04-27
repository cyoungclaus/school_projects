import const
import tkinter as tk
from const import root

title = tk.Label(text="551 project")
title.pack()

frame = tk.Frame(master=root, width=800, height=300)
frame.pack()

yButtons = 100

# First Function - Lyrics Generator
button1 = tk.Button(
    master=frame,
    text="Game:\nGet Random Song Lyrics",
    command=lambda: const.getLyrics(),
    bg="gray",
    fg="black",
)
button1.place(x=100, y=yButtons)

# Second Function - Playlist Randomizer
button2 = tk.Button(
    master=frame,
    text="Game:\nSong/Playlist Guesser",
    command=lambda: const.playlists(frame),
    bg="gray",
    fg="black",
)
button2.place(x=300, y=yButtons)

"""

# Third Function - Song Vizualizer
button3 = tk.Button(
    master=frame,
    text="3: Song",
    bg="gray",
    fg="black",
)
button3.place(x=600,y=500)

button4 = tk.Button(
    master=frame,
    text="4: Rebuild",
    bg="gray",
    fg="black",
)
button3.place(x=800,y=500)
"""

root.mainloop()
