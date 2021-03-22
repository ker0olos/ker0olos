#!/usr/bin/env bash

DEFAULT_NAME="$HOME/Pictures/Wall/default.jpg"

if [[ "$1" == "-u" ]]; then
  # create copies to the new wallpaper file
  cp "$2" "$DEFAULT_NAME" -f

  # set the picture as the current active wallpaper
  feh --bg-fill "$DEFAULT_NAME"

  # update notification

  ACTION=$(dunstify -i "$DEFAULT_NAME" "Your wallpaper" "<b>Just got updated</b>" -u low --action="default,Open")

  # when clicked open the wallpaper in default app
  case "$ACTION" in
  "default")
    xdg-open "$DEFAULT_NAME"
    ;;
  esac
else
  feh --bg-fill "$DEFAULT_NAME"
fi
