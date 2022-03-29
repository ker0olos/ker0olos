#!/bin/sh

notifiy_level() {
	LEVEL=$(brightnessctl -m | awk -v FS="(,|%)" '{print $4}')

	dunstify -r 500 -a light-shortcut "󰃠" "<b>${LEVEL}%</b>"
}

case $1 in
up)
	brightnessctl set +5%
	notifiy_level
	;;
down)
	brightnessctl set 5%-
	notifiy_level
	;;
*) ;;
esac
