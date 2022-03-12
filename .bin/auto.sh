#!/bin/sh

while true
do
    CAPS=$(xset q | grep "Caps")
    CAPS=${CAPS:21:2}
    if [ "$CAPS" = "on" ]; then
        xdotool click 1
    fi
    sleep 0.05
done