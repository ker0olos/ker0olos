#!/usr/bin/env bash

if [[ "$1" == "-u" ]]; then
  mkdir -p "$HOME/Pictures/.wall"
  touch "$HOME/Pictures/.wall/default"

  # set the picture as the current active wallpaper
  if [[ "$3" == "-p" ]]; then
    feh --bg-fill "$2" --bg-fill "$4"
    echo "wall.sh -u $2 -p $4" > "$HOME/Pictures/.wall/default"
  else
    feh --bg-fill "$2"
    echo "wall.sh -u $2" > "$HOME/Pictures/.wall/default"
  fi

  # update notification

  ACTION=$(dunstify -i "$2" "Your wallpaper" "<b>Just got updated</b>" -u low --action="default,Open")

  # when clicked open the wallpaper in default app
  case "$ACTION" in
  "default")
    xdg-open "$2"
    ;;
  esac
else
  sh -c "$(cat $HOME/Pictures/.wall/default)"
fi
