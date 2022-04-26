#from settings import sp, genius, CLIENT_ID, CLIENT_SECRET, CLIENT_NAME, LIKED_SONGS, PLAYLISTS, getLikedSongs, getPlaylists
import settings as i
from settings import sp, genius

import tkinter as tk
from tkinter import *
from tkinter import ttk

# Build
# ================
f = open(i.LIKED_SONGS, 'r')
if f.read().split('\n', 1)[0] == '':
    i.getLikedSongs()
f.close()

f = open(i.PLAYLISTS, 'r')
if f.read().split('\n', 1)[0] == '':
    i.getPlaylists()
f.close()
# ================

root = Tk()

# Get lyrics for song by NAME and print them to screen
def getLyrics(frame, title, artist):
    song = genius.search_song(title=title, artist=artist)
    #frame.destroy()

    container=ttk.Frame(root)
    container.tkraise()
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    ttk.Label(scrollable_frame, text=song.lyrics).pack()

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    back = tk.Button(
        master=scrollable_frame,
        text="Back",
        command=lambda: container.destroy(),
        bg="gray",
        fg="black",
    )
    back.pack()



# Grab a random playlist ID from playlists.txt
def getRandPlaylist():
    pass

# Get all songs from a playlist ID


def getTracks(playlist):
    tracks = sp.user_playlist_tracks(i.CLIENT_NAME, playlist)
    songs = tracks['items']
    ids = []

    while tracks['next']:
        tracks = sp.next(tracks)
        songs.extend(tracks['items'])
    for song in songs:
        ids.append(song['track']['id'])

    return ids