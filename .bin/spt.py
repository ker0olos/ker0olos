#!/bin/python

import os
import sys

import spotipy

command = sys.argv[1] if len(sys.argv) > 1 else sys.exit()

curr_name = "Space"

try:
    spotify = spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://localhost:8870/callback",
            cache_path=os.environ["HOME"] + "/sptpy_token.json",
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
        print("Getting recently played tracks")
        recently_played = spotify.current_user_recently_played(limit=50)
        recently_played_uris = list(
            map(lambda v: v["track"]["uri"], recently_played["items"])
        )

        print(f"Looking for {curr_name}")
        devices = spotify.devices()["devices"]
        space_id = None

        for d in devices:
            if d["name"] == curr_name:
                space_id = d["id"]
                break

        if space_id is None:
            print(f"{curr_name} not found")
            sys.exit()

        spotify.start_playback(space_id, uris=recently_played_uris)
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
