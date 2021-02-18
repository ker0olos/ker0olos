#!/bin/bash

while true
do
    sleep 2
    xdotool type "document.body.querySelectorAll('.select_pink')[1].click()"
    xdotool key Return
    
    sleep 3
    xdotool type "document.body.querySelector('.select_pink_long').click()"
    xdotool key Return
done
