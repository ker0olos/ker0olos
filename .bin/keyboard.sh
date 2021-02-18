#!/usr/bin/env bash

if [[ $(setxkbmap -print | awk -F"+" '/xkb_symbols/ {print $2}') == 'us' ]]; then
	setxkbmap ar
	dunstify -r 500 -a keyboard-shortcut "" "<b>Keyboard Layout</b>\nArabic"
else
	setxkbmap us
	dunstify -r 500 -a keyboard-shortcut "" "<b>Keyboard Layout</b>\nEnglish"
fi
