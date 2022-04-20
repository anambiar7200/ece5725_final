""" Anusha Nambiar (aan29), Alisha Kochar (ak225)
ECE 5725 final project 
"""

import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
import random

DEVICE_ID = "8496ca001c12ab095280d2919c55501bb1310cb0"
SPOTIPY_CLIENT_ID = "7b651d6263ea4ec79a0fc0f879b52fee"
SPOTIPY_CLIENT_SECRET= "e46a9c327fe346068652404d83b763a5"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri="http://localhost:8080",
                                               #redirect_uri="http://google.com/",
                                               scope="user-read-playback-state,user-modify-playback-state"))

# Shows playing devices
# res = sp.devices()
# pprint(res)

# plays song even if device not currently active
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

# get album list
tracks = sp.album_tracks('album_id=spotify:album:3vUL7XVv8gsxuIFbamidAn', limit=50, offset=0, market=None)

# get each song ID
songs = []
for i in range(len(tracks.get('items'))):
    id = tracks.get('items')[i].get('id')
    songs.append(id)

# randomly choose one of the songs to play
random_track = random.randint(0,len(songs)-1)

# get the song's ID and play it
id = songs[random_track]
sp.start_playback(uris=['spotify:track:'+str(id)])

# Change track
# sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

# Change volume
# sp.volume(100)
# time.sleep(2)
# sp.volume(50)
# time.sleep(2)
# sp.volume(100)