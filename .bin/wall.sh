#!/bin/sh

if [[ $1 == "-u" ]]; then
	mkdir -p "${HOME}/Pictures/.wall"
	touch "${HOME}/Pictures/.wall/default"

	# set the picture as the current active wallpaper
	if [[ $3 == "-p" ]]; then
		feh --bg-fill "$2" --bg-fill "$4"
		echo "wall.sh -u $2 -p $4" >"${HOME}/Pictures/.wall/default"
	else
		feh --bg-fill "$2"
		echo "wall.sh -u $2" >"${HOME}/Pictures/.wall/default"
	fi

	# sent a notification with dunst with a preview of the wallpaper
	dunstify -i "$2" "Your wallpaper" "<b>Just got updated</b>" -u low
elif [[ $1 == "bookmark" ]]; then
	cp "${HOME}/Pictures/.wall/default" "${HOME}/Pictures/.wall/.bookmarks/$2"
	echo "Bookmarked current wallpaper as \"$2\""
elif [[ $1 == "ls" ]]; then
	ls "${HOME}/Pictures/.wall/.bookmarks/$2"
else
	if [[ -n $1 && -f "${HOME}/Pictures/.wall/.bookmarks/$1" ]]; then
		cp "${HOME}/Pictures/.wall/.bookmarks/$1" "${HOME}/Pictures/.wall/default"
		echo "Updating to the bookmarked wallpaper \"$1\""
	fi

	sh -c "$(cat "${HOME}"/Pictures/.wall/default)"
fi
