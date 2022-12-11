#!/bin/bash

# desktop_id=$(echo "$1" | awk '{print $3}')
# monitor_id=$(echo "$1" | awk '{print $2}')
# node_id=$(echo "$1" | awk '{print $5}')

is_empty_desktop=$(bspc query -D -d 'focused.occupied')

if [ -z "$is_empty_desktop" ]; then
    bspc desktop -f last.occupied.local 
fi

# for debugging purposes
# notify-send "$1" "$desktop_id"
