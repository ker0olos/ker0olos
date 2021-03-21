#!/usr/bin/env bash

DEFAULT_NAME="$HOME/Pictures/Wall/default.jpg"

# set previous wall as placeholder
feh --bg-fill "$DEFAULT_NAME"

if [[ "$1" == "-u" ]]; then
  # Using Reddit API

  [ ! -d "$HOME/Pictures/Wall" ] && mkdir "$HOME/Pictures/Wall"

  # UwU <3
  FILE_NAME=$(wall.py Animewallpaper)

  # Set the picture as wallpaper

  # create copies to the new wallpaper file
  cp "$FILE_NAME" "$DEFAULT_NAME" -f

  # set the picture as the current active wallpaper
  feh --bg-fill "$FILE_NAME"

  # update notification

  ACTION=$(dunstify -i "$FILE_NAME" "Your wallpaper" "<b>Just got updated</b>" -u low --action="default,Open")

  # when clicked open the wallpaper in default app
  case "$ACTION" in
  "default")
    xdg-open "$FILE_NAME"
    ;;
  esac
fi
