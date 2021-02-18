#!/usr/bin/env bash

liked=$(sptctl liked)

if [ "$liked" = 1 ]; then
  echo "󰋑"
else
  echo "󰋕"
fi