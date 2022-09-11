#!/bin/bash

percentage=$(bluetoothctl info | grep 'Battery Percentage')

if [ -z "$percentage" ]; then
	echo "" 
else
	percentage=$(echo "$percentage" | awk '{print substr($0,22,4) }')
    percentage=$(printf "%d\n" "$percentage")
    echo "$percentage%%{T3}󰋋%{T-}"
fi