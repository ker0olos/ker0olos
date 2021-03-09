#!/usr/bin/env bash

function cleanup()
{
  xdo kill -N 'Spotify'
  xdo kill -a 'polybar-spotify_eDP-1'
  # xdo kill -a 'polybar-spotify2_eDP-1'
}

# Title & Like Button
(sleep 4 && polybar spotify) &
# Progress Bar
# (sleep 3 && polybar spotify2) &

/usr/bin/spotify

trap cleanup EXIT
