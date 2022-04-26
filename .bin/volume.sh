#!/bin/bash

MUTED=$(pamixer --get-mute)

notifiy_mute() {
	# ICON=󰖁

	if [[ ${MUTED} == "true" ]]; then
		dunstify -r 500 -a volume-shortcut "" "<b><i>unmuted</i></b>"
	else
		dunstify -r 500 -a volume-shortcut "" "<b><i>muted</i></b>"
	fi
}

notifiy_level() {
	ICON=󰕿

	LEVEL=$(pamixer --get-volume)

	if ((LEVEL >= 70)); then
		ICON=󰕾
	elif ((LEVEL >= 35)); then
		ICON=󰖀
	fi

	dunstify -r 500 -a volume-shortcut "${ICON}" "<b>${LEVEL}%</b>"
}

case $1 in
up)
	pamixer -i 5 --allow-boost
	pamixer -u
	notifiy_level
	;;
down)
	pamixer -d 5 --allow-boost
	pamixer -u
	notifiy_level
	;;
mute)
	pamixer -t
	notifiy_mute
	;;
*) ;;
esac
