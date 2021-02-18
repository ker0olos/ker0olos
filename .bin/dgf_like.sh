#!/bin/bash

while true
do
    sleep 2
    xdotool type "document.body.querySelectorAll('.select_pink')[1].click()"
    xdotool key Return
    
    sleep 2
    xdotool type "document.body.querySelector('.select_pink_middle').click()"
    xdotool key Return
done
