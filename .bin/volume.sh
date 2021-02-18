#!/usr/bin/env bash

MUTED=$(pulseaudio-ctl | grep -o 'Is sink muted.*:.*' | sed 's/\x1B\[[0-9;]\+[A-Za-z]//g' | awk '{print substr($0,20,3) }')

function unmute {
  if [[ "$MUTED" = "yes" ]]; then
    pulseaudio-ctl mute
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

  LEVEL=$(pulseaudio-ctl | grep -o 'Volume level.*:.*' | sed 's/\x1B\[[0-9;]\+[A-Za-z]//g' | awk '{print substr($0,20)}')
  LEVEL="${LEVEL/\%/}"

  if (( $LEVEL >= 70 )); then
    ICON=󰕾
  elif (( $LEVEL >= 35 )); then
    ICON=󰖀
  fi
  dunstify -r 500 -a volume-shortcut "$ICON" "<b>$LEVEL%</b>"
}

case $1 in
    up)
	  pulseaudio-ctl up
    unmute
    notifiy_level
	;;
    down)
	  pulseaudio-ctl down
    unmute
    notifiy_level
	;;
    mute)
	  pulseaudio-ctl mute
    notifiy_mute
	;;
esac