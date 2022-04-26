#!/bin/bash

STATE=$(dunstctl is-paused)

if [ "$1" = "toggle" ]; then
	dunstctl set-paused toggle
fi

if [ "${STATE}" = "false" ]; then
	echo "󰂚"
else
	echo "%{F#ffd200}󰪑%{F-}"
fi
