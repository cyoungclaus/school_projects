import const
import build
import tkinter as tk
from const import root

title = tk.Label(text="551 project")
title.pack()

frame = tk.Frame(master=root, width=1000, height=600)
frame.pack()

# First Function - Lyrics Generator
button1 = tk.Button(
    master=frame,
    text="B1",
    command=lambda: build.lyrics(frame),
    bg="gray",
    fg="black",
)
button1.place(x=100, y=500)

# Second Function - Playlist Randomizer
button2 = tk.Button(
    master=frame,
    text="2: Playlist",
    bg="gray",
    fg="black",
)
button2.place(x=800, y=500)

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
