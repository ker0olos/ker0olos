#!/bin/python

import os
import sys
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# parse arguments
if len(sys.argv) > 1:
  command = sys.argv[1]
else:
  sys.exit()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri='http://localhost:8888/callback',
                                               cache_path='./.spotify_cache',
                                               scope='user-read-playback-state,user-modify-playback-state,user-library-read,user-library-modify,user-read-recently-played'))

active=True
currently_playing=spotify.currently_playing()

# nothing is playing
# output info about last recently played track
if (not currently_playing):
  active=False
  currently_playing={
    'is_playing': False,
    'item': spotify.current_user_recently_played(limit=1)['items'][0]['track']
  }

tid=currently_playing['item']['id']

if (command=='title'):
  print(currently_playing['item']['name'])
elif (command=='toggle'):
  if currently_playing['is_playing']:
    spotify.pause_playback()
  elif not active:
    devices=spotify.devices()['devices']
    if (len(devices) == 0):
      print('No devices available.')
      sys.exit()
    # last streamed 40 tracks
    uris=map(lambda item: item['track']['uri'], spotify.current_user_recently_played(limit=40)['items'])
    spotify.start_playback(device_id=devices[0]['id'],uris=list(uris))
  else:
    spotify.start_playback()
elif (command=='skip'):
  spotify.next_track()
# elif (command=='previous'):
#   spotify.previous_track()
# elif (command=='shuffle'):
#   spotify.shuffle(not spotify.current_playback()['shuffle_state'])
elif (command=='state'):
  print('󰋑') if spotify.current_user_saved_tracks_contains(tracks=[tid])[0] else print('󰋕')
elif (command=='like'):
  if not spotify.current_user_saved_tracks_contains(tracks=[tid])[0]:
    spotify.current_user_saved_tracks_add(tracks=[tid])
  else:
    spotify.current_user_saved_tracks_delete(tracks=[tid])