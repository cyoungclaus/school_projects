import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius as lg

# Initialization
# -------------------------
CLIENT_ID = '9a0a84b0ed4443ed8e8e4014f4d3edbb'
CLIENT_SECRET = '93bf0299df4442af92dfafc475e2c21a'
CLIENT_NAME = 'dublecy'

# =============
# client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# =================

# This is temporarily only using my Spotify account
# until I can have the user authenticate themselves
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:9000", scope="user-library-read playlist-read-private"))
api_key = "I9nL4VjfIFb97CrIlDKgTgDHHURCfi3BrvD2700v4M4y8vIqkfyxdQuyMkV5nPVY"
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

# -------------------------

# First-time Build
#   Gets user's information and writes them all 
#   to likedsongs.txt and playlists.txt

LIKED_SONGS = "C:\\Users\\StevensUser\\Desktop\\551pythonFP\\store\\liked_songs.txt"
PLAYLISTS = "C:\\Users\\StevensUser\\Desktop\\551pythonFP\\store\\playlists.txt"

def getLikedSongs():
    first = sp.current_user_saved_tracks(limit=1)
    tracks = sp.current_user_saved_tracks(limit=50)
    first_line = ''
    x = 0
    numError = 0
    for i, track in enumerate(first['items']):
        first_song = str(track['track']['id']) + ";" + str(track['track']['name']) + ";" + str(track['track']['artists'][0]['name']) + "\n"
    
    f = open(LIKED_SONGS, 'r')
    first_line = f.read().split('\n', 1)[0]
    f.close()

    print("Updating Liked Songs...")
    f = open(LIKED_SONGS, 'w')
    while x < 100:       # Will only save up to 5000 liked songs
        try:
            tracks = sp.current_user_saved_tracks(limit=50,offset=x*50)
            for i, track in enumerate(tracks['items']):
                line = str(track['track']['id']) + ";" + str(track['track']['name']) + ";" + str(track['track']['artists'][0]['name']) + "\n"
                f.write(line)
        except:
            print("Error song: " + line)
            numError += 1
        finally:
            x+=1
    f.close()
    print("Build complete with " + str(numError) + " errors.")

def getPlaylists():
    playlists = sp.user_playlists(CLIENT_NAME)
    f = open(PLAYLISTS, 'w')

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            line = str(playlist['uri'] + ";" + str(playlist['name'] + "\n"))
            try:
                f.write(line)
            except:
                print("Error with " + str(playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    f.close()