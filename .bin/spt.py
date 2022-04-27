#!/bin/python

import os
import sys
import math
import time
import datetime
import subprocess
import http.client as httplib

import psutil
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def running(name):
    for proc in psutil.process_iter():
        try:
            if name in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# parse arguments
if len(sys.argv) > 1:
    command = sys.argv[1]
else:
    sys.exit()

connection = httplib.HTTPConnection("api.spotify.com", timeout=1)

try:
    connection.request("HEAD", "/")
    connection.close()
except Exception:
    print("No internet connection") if command == "title" else print("")
    connection.close()
    sys.exit()

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:8870/callback",
        cache_path=os.environ["HOME"] + "/.spotify_cache",
        scope="user-read-playback-state,user-modify-playback-state,user-library-read,user-library-modify,user-read-recently-played",
    )
)

currently_playing = spotify.currently_playing()

playlists = [
    # https://open.spotify.com/genre/made-for-x-hub
    ["spotify:playlist:37i9dQZF1E35tuHOcRhgZZ", "Daily Mix 1"],
    ["spotify:playlist:37i9dQZF1E3855z4z5OsPs", "Daily Mix 2"],
    ["spotify:playlist:37i9dQZF1E39jZuNJB5bh7", "Daily Mix 3"],
    ["spotify:playlist:37i9dQZF1E36Hq1lYk3e5n", "Daily Mix 4"],
    ["spotify:playlist:37i9dQZF1DWV4t1PmvRVd9", "Egyptian Indie"],
    ["spotify:playlist:37i9dQZF1DX2siSxlNkZrf", "Black Zone"],
    # [ 'spotify:playlist:37i9dQZEVXbsA9iS8lxmLk', 'Release Radar' ],
    # [ 'spotify:playlist:37i9dQZF1DWUQM3rmTXpBR', 'Arab Indie' ],
]

# nothing is playing
if not currently_playing or command == "skip" or command == "play":
    id = min(
        max(math.ceil(int(datetime.datetime.utcnow().strftime("%S")) / 10) - 1, 0),
        len(playlists) - 1,
    )

    if command == "title":
        print(playlists[id][1])
    elif command == "toggle" or command == "skip" or command == "play":
        devices = spotify.devices()["devices"]

        if not running("spotifyd") or len(devices) == 0:
            subprocess.Popen(["spotifyd"])
            time.sleep(1)
            devices = spotify.devices()["devices"]

        if command == "play":
            for i, item in enumerate(playlists):
                print("{}) {}".format(i, item[1]))
            id = int(input("Make your choice: "))

        spotify.start_playback(device_id=devices[0]["id"], context_uri=playlists[id][0])

        spotify.shuffle(True)
        spotify.repeat("context")

        spotify.next_track()
    else:
        print("")
else:
    tid = currently_playing["item"]["id"]

    if command == "title":
        print(currently_playing["item"]["name"])
    elif command == "toggle":
        if currently_playing["is_playing"]:
            spotify.pause_playback()
        else:
            spotify.start_playback()
    elif command == "previous":
        spotify.previous_track()
    elif command == "state":
        print("󰋑") if spotify.current_user_saved_tracks_contains(tracks=[tid])[
            0
        ] else print("󰋕")
    elif command == "like":
        if not spotify.current_user_saved_tracks_contains(tracks=[tid])[0]:
            spotify.current_user_saved_tracks_add(tracks=[tid])
        else:
            spotify.current_user_saved_tracks_delete(tracks=[tid])
