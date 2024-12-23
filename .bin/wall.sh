#!/bin/bash

mkdir -p "${HOME}/Pictures/.wall"
touch "${HOME}/Pictures/.wall/default"

if [[ $1 == "-u" ]]; then
	# set the picture as the current active wallpaper
	# feh --no-fehbg --bg-fill "$2" "$3" 
	gsettings set org.gnome.desktop.background picture-uri \"$2\"
	gsettings set org.gnome.desktop.background picture-uri-dark \"$2\"

	echo "wall.sh -u $2 $3" >"${HOME}/Pictures/.wall/default"

	# sent a notification with dunst with a preview of the wallpaper
	# dunstify -i "$2" "Your wallpaper" "<b>Just got updated</b>" -u low
elif [[ -z "$1" ]]; then
	sh -c "$(cat "${HOME}"/Pictures/.wall/default)"
else
	if [[ -f "${HOME}/Pictures/.wall/.bookmarks/$1" ]]; then
		cp "${HOME}/Pictures/.wall/.bookmarks/$1" "${HOME}/Pictures/.wall/default"
		sh -c "$(cat "${HOME}"/Pictures/.wall/default)"
	else
		mkdir -p "${HOME}/Pictures/.wall/.bookmarks"
		cp "${HOME}/Pictures/.wall/default" "${HOME}/Pictures/.wall/.bookmarks/$1"
		echo "Bookmarked: \"$1\""
	fi
fi
