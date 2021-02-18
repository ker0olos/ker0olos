#!/usr/bin/env bash

crunch_appname=$(echo "$1" | sed  '/^$/d')
crunch_summary=$(echo "$2" | sed  '/^$/d' | tr $'\n' ' ')
crunch_body=$(echo "$3" | sed  '/^$/d' | tr $'\n' ' ')
crunch_icon=$(echo "$4" | sed  '/^$/d')
crunch_urgency=$(echo "$5" | sed  '/^$/d')

timestamp=$(date +"%I:%M %p")

# if [[ "$crunch_appname" == "Spotify" ]]; then
#   random_name=$(mktemp --suffix ".png")
#   artlink=$(sptctl artUrl)
#   curl -s "$artlink" -o "$random_name"
#   crunch_icon=$random_name
# fi

# ignore my system notifications  
if [[ "$crunch_appname" == *-shortcut ]]; then
  echo ""
else
  echo -en "$timestamp\n$crunch_urgency\n$crunch_icon\n$crunch_body\n$crunch_summary\n$crunch_appname\n" >> /tmp/dunstlog
fi

#echo "$crunch_appname\n$crunch_summary\n$crunch_body\n$crunch_icon\n$crunch_urgency\x0f" >> /tmp/dunstlog