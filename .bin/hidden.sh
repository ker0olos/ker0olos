#!/bin/bash

WID="$(bspc query -N -n .local.hidden)"

if [ -z $WID ]; then
  echo "-"
else
  xprop -id $WID | grep WM_CLASS | awk '{print $4}' | sed -E 's/(^.)|(.$)//g' # | zscroll | sed '$d'
fi