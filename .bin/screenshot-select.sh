#!/bin/sh

cd ~/Pictures/Screenshots || exit

# take an interactive screenshot using scrot
SCREENSHOT=$(scrot -e 'echo $f' -f -s --line style=solid,width=3)

if [[ ${SCREENSHOT} == *".png" ]]; then
	# copy the screenshot to the clipboard
	xclip -selection clipboard -t image/png -i "${PWD}/${SCREENSHOT}"

	# sent a notification with dunst with a preview of the screenshot
	# and as a feedback that the screenshot was taken successfully
	ACTION=$(dunstify -a screenshot-app -i "${PWD}/${SCREENSHOT}" "Screenshot" "Copied to clipboard" --action="default,Open")

	# when clicked open the screenshot in default app
	case "${ACTION}" in
	"default")
		xdg-open "${PWD}/${SCREENSHOT}"
		;;
	*) ;;
	esac
else
	echo "Screenshot aborted"
fi
