#!/bin/sh

wid="$1"
class="$2"
instance="$3"

title="$(xtitle "$wid")"

[ -z "$class" ] && [ -z "$instance" ] && [ "$title" = "Picture in picture" ] \
    && echo 'state=floating rectangle=520x240+780+450'