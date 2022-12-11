#!/bin/bash

wid="$1"
class="$2"
# instance="$3"
eval "$4"

# current_desktop=$(bspc query -D -d 'focused')
next_empty_desktop=$(bspc query -D -d 'next.!occupied')

if [ -z "$class" ]; then
    # use title if window_class is not specified
    class="$(xtitle "${wid}")"
fi

case "${class}" in
    # peek is an edge-case that needs to float above the current desktop
    "Peek")
        echo "state=floating rectangle=640x480+0+0 focus=on center=on" ;;
    # pip is about the same as peek but with a specified position
    "Picture in picture")
        picom-trans -w "$wid" -o 100
        echo "state=floating rectangle=520x240+780+450 focus=off" ;;
    
    # move any non-centered nodes to the next empty desktop
    *) if [ "${center:?}" != "on" ]; then
        echo "desktop=$next_empty_desktop follow=on"
    fi ;;
esac

# extra node rules per class
case "${class}" in
    "Alacritty") echo "state=pseudo_tiled" ;;
esac

# for debugging purposes
# notify-send "\$1=$(printf '0x%08X' "$1") \$2=$2 \$3=$3" "$4"

