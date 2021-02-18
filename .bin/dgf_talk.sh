#!/bin/bash

while true
do
    sleep 1
    xdotool type "document.body.querySelector('.select_pink_middle').click()"
    xdotool key Return
done
