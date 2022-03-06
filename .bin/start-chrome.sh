#!/usr/bin/env bash

if [[ "$1" == "--incognito" ]]; then
  google-chrome-stable $2 --enable-features=WebUIDarkMode --force-dark-mode --incognito
else
  google-chrome-stable $1 --enable-features=WebUIDarkMode --force-dark-mode
fi