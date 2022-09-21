#!/bin/bash

# WID="$(bspc query -N -n .local.hidden)"
WORKSPACE="$(bspc query -D -d focused --names)"

# if [ -z $WID ]; then
#   echo "$WORKSPACE"
# else
#   echo "$WORKSPACE" "$(xprop -id $WID | grep WM_CLASS | awk '{print $4}' | sed -E 's/(^.)|(.$)//g')"
# fi

echo "$WORKSPACE"