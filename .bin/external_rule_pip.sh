#!/bin/sh

wid="$1"
class="$2"
instance="$3"

title="$(xtitle "${wid}")"

external_monitor_1=$(xrandr --query | grep 'VGA-1-1')

# if no window class is defined
if [ -z "${class}" ] && [ -z "${instance}" ]; then
	case "${title}" in
	"Picture in picture")
		if [[ ${external_monitor_1} == "VGA-1-1 connected"* ]]; then
			echo 'state=floating rectangle=520x240+1840+450'
		else
			echo 'state=floating rectangle=520x240+780+450'
		fi
		;;
	"cv2") echo 'state=pseudo_tiled' ;;
	*) echo 'state=tiled' ;;
	esac
fi
