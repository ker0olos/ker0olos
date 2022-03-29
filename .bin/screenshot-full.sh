#!/bin/sh

cd ~/Pictures/Screenshots || exit

# take a full screenshot using scrot
SCREENSHOT=$(scrot -e 'echo $f')

if [[ ${SCREENSHOT} == *".png" ]]; then
	# copy the screenshot to the clipboard
	xclip -selection clipboard -t image/png -i "${PWD}/${SCREENSHOT}"

	# sent a notification with dunst with a preview of the screenshot
	dunstify -a screenshot-app -i "${PWD}/${SCREENSHOT}" "Screenshot" "Copied to clipboard"
else
	echo "Screenshot aborted"
fi
