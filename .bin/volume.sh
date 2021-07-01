#!/usr/bin/env bash

MUTED=$(pamixer --get-mute)

function unmute {
  if [[ "$MUTED" = "true" ]]; then
	  pamixer -t
  fi
}

function notifiy_mute {
  # ICON=󰖁

  if [[ "$MUTED" = "yes" ]]; then
    dunstify -r 500 -a volume-shortcut "" "<b><i>unmuted</i></b>"
  else
    dunstify -r 500 -a volume-shortcut "" "<b><i>muted</i></b>"
  fi
}

function notifiy_level {
  ICON=󰕿

  LEVEL=$(pamixer --get-volume)

  if (( $LEVEL >= 70 )); then
    ICON=󰕾
  elif (( $LEVEL >= 35 )); then
    ICON=󰖀
  fi

  dunstify -r 500 -a volume-shortcut "$ICON" "<b>$LEVEL%</b>"
}

case $1 in
    up)
	  pamixer -i 5
    unmute
    notifiy_level
	;;
    down)
	  pamixer -d 5
    unmute
    notifiy_level
	;;
    mute)
	  pamixer -t
    notifiy_mute
	;;
esac