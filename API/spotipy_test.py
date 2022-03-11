# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 09:46:46 2021

@author: AD
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='', client_secret=''))

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']

album_number = 1
album_index = album_number - 1

album_artist_dict = albums[album_index]["artists"][0] # no need to specify artist index as the only artist on album

print(albums[album_index]['name'])
print(albums[album_index]['release_date'])
print(albums[album_index]['total_tracks'])
print(albums[album_index]['type'])