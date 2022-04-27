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
        master=canvas,
        text="Back",
        command=lambda: container.destroy(),
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

def playlists(frame):
    correctPlaylist = getRandPlaylist()
    song = random.choice(getTracks(correctPlaylist))
    playlistAnswer = playlistArray[0]
    f = open(PLAYLISTS, 'r')
    idHolder = ''
    index = 0
    counter = 0
    random.shuffle(playlistArray)

    container = ttk.Frame(root)
    container.tkraise()
    canvas = tk.Canvas(container)
    canvas.create_window((0,0), anchor="w")

    titleHolder = sp.track(song)["name"]
    title = Label(container, text="\nWhat playlist did we get \"" + titleHolder + "\" by " + sp.track(song)['artists'][0]['name'] + " from?")
    title.pack()

    canvas.pack(side="left", fill="both", expand=True)
    
    gridCanvas = tk.Canvas(container)
    gridFrame = ttk.Frame(gridCanvas)

    gridCanvas.create_window((0,0), window=gridFrame, anchor='nw')
    
    selection = 0

    for x in range(0, len(playlistArray)):
        button = tk.Button(
            master=gridFrame,
            text= str(x+1) + ") " + playlistArray[x],
            bg="gray",
            fg="black",
        )
        button.grid(row=0, column=x)
        #print(str(x+1) + ") " + playlistArray[x])
    
    """
    print('')
    answer = input("--> ") 
    while True:
        if (answer == playlistAnswer) or (int(answer) == playlistArray.index(playlistAnswer)+1):
            print("--> Correct")
            counter += 1
            return True
        elif (answer not in playlistArray) and (int(answer) not in range(1,5)):
            answer = input("Invalid input --> ")
        else:
            for item in playlistArray:          #this part is extremely slow - needs efficiency
                for line in f:
                    index+=1
                    if item in line.split(';')[1]:
                        idHolder = line.split(':')[2].split(';')[0]
                for item in getTracks(idHolder):
                    if sp.track(song)['id'] == item:
                        print("--> Correct, but song was pulled from " + playlistAnswer)
                        counter += 1
                        return True
            print("--> Incorrect. Answer was " + playlistAnswer)
            print("You got through " + str(counter) + " songs.")
            return False
    """
    back = tk.Button(
        master=gridFrame,
        text="Back",
        command=lambda: container.destroy(),
        bg="gray",
        fg="black",
    )
    back.grid(row=1, columnspan=3)

    gridCanvas.pack()
    container.pack()

    
    