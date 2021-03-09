#!/usr/bin/env bash

if [[ -n "$( echo "$1" | grep -o -P "\p{Arabic}" )" ]]; then
  S="$1"
  S="${S/)/(}"
  S="${S/(/)}"
  echo "$S" | ara
else
  echo "$1"
fi