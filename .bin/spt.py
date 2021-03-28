#!/bin/python

import os
import sys
import time
import random
import subprocess

import http.client as httplib

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# parse arguments
if len(sys.argv) > 1:
  command = sys.argv[1]
else:
  sys.exit()

connection = httplib.HTTPConnection('api.spotify.com', timeout=1)

try:
  connection.request('HEAD', '/')
  connection.close()
except:
  print('No internet connection.') if command=='title' else print('')
  connection.close()
  sys.exit()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri='http://localhost:8888/callback',
                                               cache_path=os.environ['HOME']+'/.spotify_cache',
                                               scope='user-read-playback-state,user-modify-playback-state,user-library-read,user-library-modify,user-read-recently-played'))

currently_playing=spotify.currently_playing()

# nothing is playing
# output info about last recently played track
if (not currently_playing):
  if (command=='title'):
    print('Nothing is queued.')
    # print(spotify.current_user_recently_played(limit=1)['items'][0]['track']['name'])
  elif (command=='toggle'):
    devices=spotify.devices()['devices']

    # try spawning spotifyd if there's working devices
    if (len(devices) == 0):
      subprocess.Popen(['spotifyd'])
      time.sleep(1)
      devices=spotify.devices()['devices']
      
    if (len(devices) == 0):
      print('No devices available.')
      sys.exit()

    # my favorite playlists
    uris=map(lambda item: item['track']['uri'], spotify.playlist_items(random.choice([
      'spotify:playlist:37i9dQZF1E35tuHOcRhgZZ',
      'spotify:playlist:37i9dQZF1E3855z4z5OsPs',
      'spotify:playlist:37i9dQZF1E39jZuNJB5bh7',
      'spotify:playlist:37i9dQZF1E36Hq1lYk3e5n',
      'spotify:playlist:37i9dQZF1E39KFXWlmzgOy', 
      'spotify:playlist:37i9dQZF1E35TMnPZZpmYQ',
      'spotify:playlist:37i9dQZF1DWV4t1PmvRVd9',
      'spotify:playlist:37i9dQZF1DWUQM3rmTXpBR'
    ]))['items']) # https://open.spotify.com/genre/made-for-x-hub
    
    # get last streamed 40 tracks (little buggy for whatever fucking reason, I don't care anymore.)
    # uris=dict.fromkeys(map(lambda item: item['track']['uri'], spotify.current_user_recently_played(limit=40)['items']))

    spotify.start_playback(device_id=devices[0]['id'],uris=list(uris))

    # this is my personal preference
    spotify.shuffle(True)
    spotify.repeat('context')
  else:
    print('')
else:
  tid=currently_playing['item']['id']

  if (command=='title'):
    print(currently_playing['item']['name'])
  elif (command=='toggle'):
    if currently_playing['is_playing']:
      spotify.pause_playback()
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