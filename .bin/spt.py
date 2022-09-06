#!/bin/python

import os
import re
import sys
import json
import time
import datetime
from random import randint

import spotipy

curr_name = "Space"
curr_date = datetime.date.today().strftime("%d/%m/%Y")
cache_path = os.environ["HOME"] + "/sptpy_cache.json"


def read_cache():
    # read current cache on disk
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cache = json.loads(f.read())

            # if the cache is older than a day
            if time.strptime(curr_date, "%d/%m/%Y") > time.strptime(
                cache["write_time"], "%d/%m/%Y"
            ):
                return update_cache()

            cache["type"] = "old"

            return cache
    else:
        return update_cache()


def update_cache():
    with open(cache_path, "w") as f:
        cache = {"write_time": curr_date}

        # cache user top items
        cache["top_tracks"] = spotify.current_user_top_tracks(limit=10)
        cache["top_artist"] = spotify.current_user_top_artists(limit=10)

        # save the cache to disk
        f.write(json.dumps(cache))

        cache["type"] = "new"

        return cache


def wrapper(s):
    if re.match(r"[\u0600-\u06FF]", s):
        import arabic_reshaper

        return arabic_reshaper.reshape(s)[::-1]

    return s


def randomize(a):
    return a[randint(0, len(a) - 1)]


# def ordinal(n):
#     # https://stackoverflow.com/a/20007730/10336604
#     return f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'


def random_stat(cache):
    r = randint(0, 9)

    track = wrapper(cache["top_tracks"]["items"][r]["name"])
    track_artist = " ft. ".join(
        map(lambda a: wrapper(a["name"]), cache["top_tracks"]["items"][r]["artists"])
    )

    track_string = randomize([f"{track} by {track_artist}"])

    return track_string


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else sys.exit()

    try:
        spotify = spotipy.Spotify(
            auth_manager=spotipy.oauth2.SpotifyOAuth(
                client_id=os.environ["SPOTIFY_CLIENT_ID"],
                client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                redirect_uri="http://localhost:8870/callback",
                cache_path=os.environ["HOME"] + "/sptpy_token.json",
                scope=",".join(
                    [
                        # https://developer.spotify.com/documentation/general/guides/authorization/scopes/
                        # toggle playback on and off
                        "user-read-playback-state",
                        "user-modify-playback-state",
                        # like and unlike current track
                        "user-library-read",
                        "user-library-modify",
                        # toggle music on with one click
                        "user-read-recently-played",
                        # show stats while idling
                        "user-top-read",
                    ]
                ),
            )
        )

        currently_playing = spotify.currently_playing()
    except Exception:
        print("No internet connection") if command == "title" else print("")
        sys.exit()

    if currently_playing is None:
        cache = read_cache()

        match command:
            case "title":
                print(random_stat(cache))
            case "toggle":
                print("Getting recently played tracks")
                recently_played = spotify.current_user_recently_played(limit=50)
                recently_played_uris = list(
                    map(lambda i: i["track"]["uri"], recently_played["items"])
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
            case _:
                print("")
    # something is currently playing
    else:
        if currently_playing["item"] is not None:
            tid = currently_playing["item"]["id"]

            match command:
                case "title":
                    track_name = wrapper(currently_playing["item"]["name"])
                    artist_name = " ft. ".join(
                        map(
                            lambda a: wrapper(a["name"]),
                            currently_playing["item"]["artists"],
                        )
                    )
                    print(f"{track_name} by {artist_name}")
                case "skip":
                    spotify.next_track()
                case "toggle":
                    spotify.pause_playback() if currently_playing[
                        "is_playing"
                    ] else spotify.start_playback()
                case "state":
                    print("󰋑") if spotify.current_user_saved_tracks_contains(
                        tracks=[tid]
                    )[0] else print("󰋕")
                case "like":
                    if not spotify.current_user_saved_tracks_contains(tracks=[tid])[0]:
                        spotify.current_user_saved_tracks_add(tracks=[tid])
                    else:
                        spotify.current_user_saved_tracks_delete(tracks=[tid])
        elif command == "title":
            print("Unsupported media type")
        else:
            print("")
