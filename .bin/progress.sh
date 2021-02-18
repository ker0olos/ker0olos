#!/usr/bin/env bash

# stolen form:
# https://stackoverflow.com/a/28044986/10336604
function progressBar
{
  let _progress=(${1}*64/${2}*64)/64
  let _left=64-$_progress

  _fill=$(printf "%${_progress}s")
  _empty=$(printf "%${_left}s")

  _fillChar="_"
  _emptyChar=""

  echo "${_fill// /${_fillChar}}${_empty// /${_emptyChar}}"
}

data=($(sptctl position,duration))

echo "$(progressBar ${data[0]} ${data[1]})"