from settings import sp, genius, CLIENT_ID, CLIENT_SECRET, CLIENT_NAME, LIKED_SONGS, PLAYLISTS, getLikedSongs, getPlaylists
import tkinter as tk
from tkinter import *
import tkinter.tix as tx

# Build
# ================
f = open(LIKED_SONGS, 'r')
if f.read().split('\n', 1)[0] == '':
    getLikedSongs()
f.close()

f = open(PLAYLISTS, 'r')
if f.read().split('\n', 1)[0] == '':
    getPlaylists()
f.close()
# ================

window = Tk()

# Get lyrics for song by NAME and print them to screen


def getLyrics(frame, title, artist):
    song = genius.search_song(title=title, artist=artist)
    frame.destroy()

    tempFrame = LabelFrame(master=window, text=song.lyrics,
                           bd=5, width=1000, height=600)
    tempFrame.pack()

    # scrollbar=Scrollbar(window)
    #scrollbar.pack(side="left", expand=True, fill="y")

    # tempFrame.config(yscrollcommand=scrollbar.set)

    back = tk.Button(
        master=tempFrame,
        text="Back",
        command=lambda: tempFrame.destroy(),
        bg="gray",
        fg="black",
    )
    back.pack()

# Grab a random playlist ID from playlists.txt


def getRandPlaylist():
    pass

# Get all songs from a playlist ID


def getTracks(playlist):
    tracks = sp.user_playlist_tracks(CLIENT_NAME, playlist)
    songs = tracks['items']
    ids = []

    while tracks['next']:
        tracks = sp.next(tracks)
        songs.extend(tracks['items'])
    for song in songs:
        ids.append(song['track']['id'])

    return ids
