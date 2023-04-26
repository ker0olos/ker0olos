#!/bin/bash

theme='style-1'

dir="$HOME/.config/rofi/launchers/type-3"

## Run
rofi \
    -show drun \
    -theme ${dir}/${theme}.rasi
