from settings import sp, genius, CLIENT_ID, CLIENT_SECRET, CLIENT_NAME, LIKED_SONGS, PLAYLISTS, getLikedSongs, getPlaylists
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random

playlistArray = ['', '', '', '']
idArr = []
nameArr = []

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

root = Tk()
title = tk.Label(text="551 project")
title.pack()

frame = tk.Frame(master=root, width=800, height=300)
frame.pack()

def onClick(destroy, func):
    destroy.pack_forget()
    try:
        func()
    finally:
        pass

# Get lyrics for song by NAME and print them to screen
def getLyrics():
    title = artist = ""
    while True:
        f = open(LIKED_SONGS).read().splitlines()
        choice = random.choice(f)
        title = str(choice.split(';')[1]).strip()
        artist = str(choice.split(';')[2]).strip()
        try:
            song = genius.search_song(title=title, artist=artist)
            break
        except:
            print("Error with getting song info. Retrying...")

    container = ttk.Frame(root)
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

    label = Label(scrollable_frame, text="Your song is: " + title + " by " + artist)
    label.pack()

    ttk.Label(scrollable_frame, text=song.lyrics).pack()

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    back = tk.Button(
        master=container,
        text="Back",
        command=lambda: onClick(container, frame.pack()),
        bg="gray",
        fg="black",
    )
    back.pack()

# Grab a random playlist ID from playlists.txt
def getRandPlaylist():
    idArr.clear()
    nameArr.clear()
    playlists = sp.user_playlists(CLIENT_NAME)
    index = 0
    maxIndex = 0
    f = open(PLAYLISTS, 'w')

    while playlists:
        for a, playlist in enumerate(playlists['items']):
            idArr.append(playlist['uri'])
            nameArr.append(playlist['name'])
            line = str(playlist['uri']) + ";" + str(playlist['name'] + "\n")
            try:
                f.write(line)
            except:
                pass
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    #print("NameArr: ")
    #print(nameArr)
    f.close()
    maxIndex = len(idArr)-1
    
    index = random.randint(0, maxIndex)
    subj = idArr[index]
    playlistArray[0] = nameArr[index]
    del(nameArr[index])
    for x in range(1, 4):
        y = random.randint(0, maxIndex)-1
        while nameArr[y] in playlistArray:
            y = random.randint(0, maxIndex)
        playlistArray[x] = nameArr[y]
        
    return subj

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

def playlists():
    correctPlaylist = getRandPlaylist()
    song = random.choice(getTracks(correctPlaylist))
    playlistAnswer = playlistArray[0]
    f = open(PLAYLISTS, 'r')
    random.shuffle(playlistArray)

    container = ttk.Frame(root)
    container.tkraise()
    canvas = tk.Canvas(container)
    canvas.create_window((0,0), anchor="nw")

    canvas.pack(side="left", fill="both", expand=True)
    
    gridCanvas = tk.Canvas(container)
    gridFrame = ttk.Frame(gridCanvas)

    gridCanvas.create_window((0,0), window=gridFrame, anchor='nw')

    titleHolder = sp.track(song)["name"]
    label = Label(container, text="\nWhat playlist did we get \"" + titleHolder + "\" by " + sp.track(song)['artists'][0]['name'] + " from?")
    label.pack()
    for x in range(0, len(playlistArray)):
        print(str(x+1) + ") " + playlistArray[x])

    label = Label(container, text="Correct: " + playlistAnswer)
    label.pack()

    def success(index):
        print("success worked")
        container.pack_forget()

        temp = ttk.Frame(root)
        temp.tkraise()
        canvas = tk.Canvas(temp)
        canvas.create_window((0,0), anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        if index == 1:
            label = Label(temp, text="Correct!")
            label.pack()
        elif index == 2:
            label = Label(temp, text="Correct, but the song is also from " + playlistAnswer)
            label.pack()
        else:
            label = Label(temp, text="Wrong! Correct answer was " + playlistAnswer)
            label.pack()

        temp.pack()
        canvas.pack(side="left", fill="both", expand=True)

        back = tk.Button(
            master=temp,
            text="Back",
            command=lambda: onClick(temp, frame.pack()),
            bg="gray",
            fg="black",
        )
        back.pack()

    def check(answer):
        #idHolder = ''
        if answer == playlistAnswer:
            success(1)
        else:
            # This part is supposed to make sure the song isn't in the
            # other three random playlists before saying the user is wrong
            # but it takes too long to iterate through each playlist and check
            """ 
            for item in playlistArray: 
                for line in f:
                    if item in line.split(';')[1]:
                        idHolder = line.split(':')[2].split(';')[0]
                for item in getTracks(idHolder):
                    if sp.track(song)['id'] == item:
                        print("success 2")
                        success(2)
            """
            success(0)

#=================================================
# This needs to be condensed to a loop; can't figure it out atm
    button = tk.Button(
        master=gridFrame,
        text= "1) + "  + playlistArray[0],
        command=lambda: check(playlistArray[0]),
        bg="gray",
        fg="black",
    )
    button.grid(row=0, column=0)

    button = tk.Button(
        master=gridFrame,
        text= "2) + "  + playlistArray[1],
        command=lambda: check(playlistArray[1]),
        bg="gray",
        fg="black",
    )
    button.grid(row=0, column=1)

    button = tk.Button(
        master=gridFrame,
        text= "3) + "  + playlistArray[2],
        command=lambda: check(playlistArray[2]),
        bg="gray",
        fg="black",
    )
    button.grid(row=0, column=2)

    button = tk.Button(
        master=gridFrame,
        text= "4) + "  + playlistArray[3],
        command=lambda: check(playlistArray[3]),
        bg="gray",
        fg="black",
    )
    button.grid(row=0, column=3)
#======================================================

    back = tk.Button(
        master=gridFrame,
        text="Back",
        command=lambda: onClick(container, frame.pack()),
        bg="gray",
        fg="black",
    )
    back.grid(row=1, columnspan=3)

    gridCanvas.pack()
    container.pack()
