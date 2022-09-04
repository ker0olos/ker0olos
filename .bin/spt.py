#!/bin/python

import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

playlists = [
    "spotify:playlist:37i9dQZF1E35tuHOcRhgZZ",  # Daily Mix 1
    "spotify:playlist:37i9dQZF1E3855z4z5OsPs",  # Daily Mix 2
    "spotify:playlist:37i9dQZF1E39jZuNJB5bh7",  # Daily Mix 3
    "spotify:playlist:37i9dQZF1DWZyonhntyFxW",  # Egyptian Rap
    "spotify:playlist:37i9dQZF1DWV4t1PmvRVd9",  # Egyptian Indie
    # "spotify:playlist:37i9dQZF1DX2siSxlNkZrf",  # Black Zone
    # "spotify:playlist:37i9dQZEVXbsA9iS8lxmLk", # Release Radar
    # "spotify:playlist:37i9dQZF1DWUQM3rmTXpBR", # Arab Indie
]

device_name = "Space"
command = sys.argv[1] if len(sys.argv) > 1 else sys.exit()

try:
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
except Exception:
    print("No internet connection") if command == "title" else print("")
    sys.exit()

if currently_playing is None:
    if command == "title":
        print("TODO - Show stats while idling")
    elif command == "toggle":
        devices = spotify.devices()["devices"]
        space_id = None

        for d in devices:
            if d["name"] == device_name:
                space_id = d["id"]
                break

        spotify.start_playback(space_id, context_uri=playlists[3])
        spotify.repeat("context", space_id)
        spotify.shuffle(True, space_id)
    else:
        print("")
# something is currently playing
else:
    if currently_playing["item"] is not None:
        tid = currently_playing["item"]["id"]

        if command == "title":
            print(currently_playing["item"]["name"])
        elif command == "skip":
            spotify.next_track()
        elif command == "toggle" and currently_playing["is_playing"]:
            spotify.pause_playback()
        elif command == "toggle":
            spotify.start_playback()
        elif command == "state":
            print("󰋑") if spotify.current_user_saved_tracks_contains(tracks=[tid])[
                0
            ] else print("󰋕")
        elif command == "like":
            if not spotify.current_user_saved_tracks_contains(tracks=[tid])[0]:
                spotify.current_user_saved_tracks_add(tracks=[tid])
            else:
                spotify.current_user_saved_tracks_delete(tracks=[tid])
    elif command == "title":
        print("Unknown Track")
    else:
        print("")
