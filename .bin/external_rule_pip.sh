#!/usr/bin/env bash

wid="$1"
class="$2"
instance="$3"

title="$(xtitle "$wid")"

external_monitor_1=$(xrandr --query | grep 'VGA-1-1')

if [ -z "$class" ] && [ -z "$instance" ] && [ "$title" = "Picture in picture" ]; then
	if [[ "$external_monitor_1" == "VGA-1-1 connected"* ]]; then
		echo 'state=floating rectangle=520x240+1840+450'
	else
		echo 'state=floating rectangle=520x240+780+450'
	fi
fi