#!/usr/bin/env bash

DEFAULT_NAME="$HOME/Pictures/Wall/default.jpg"

# set previous wall as placeholder
feh --bg-fill "$DEFAULT_NAME"

if [[ "$1" == "-u" ]]; then
  # Unsplash API 
  URL="https://api.unsplash.com/photos/random?count=1&orientation=landscape"

  # Search Terms
  [[ ! -z "$2" ]] && QUERY="query=$2" || QUERY="query=dark"

  echo "The search terms are $QUERY"

  # Unsplash API access key
  ID="client_id=64daf439e9b579dd566620c0b07022706522d87b255d06dd01d5470b7f193b8d"

  # Get a random picture from Unsplash 
  DATA=$(curl -s "$URL&$QUERY&$ID")

  # Extract json values from the response

  DOWNLOAD=$(echo $DATA | jq -r '.[0].urls.full')

  FILE_NAME=$(echo $DATA | jq -r '.[0].id')
  FILE_NAME="$HOME/Pictures/Wall/$FILE_NAME.jpg"

  # Download the picture to disk

  [ ! -d "$HOME/Pictures/Wall" ] && mkdir "$HOME/Pictures/Wall"

  curl "$DOWNLOAD" -o "$FILE_NAME"

  # Set the picture as wallpaper

  # create copies to the new wallpaper file
  cp "$FILE_NAME" "$DEFAULT_NAME" -f

  # set the picture as the current active wallpaper
  feh --bg-fill "$FILE_NAME"

  # update notification

  ACTION=$(dunstify -i "$FILE_NAME" "Your wallpaper" "<b>Just got updated</b>" -u low --action="default,Open")

  # when clicked open the wallpaper in default app
  case "$ACTION" in
  "default")
    xdg-open "$FILE_NAME"
    ;;
  esac
fi
