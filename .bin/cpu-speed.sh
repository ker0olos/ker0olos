#!/usr/bin/env bash

cpupower frequency-info | grep ': .* (' -o | awk '{print substr($0,3,8) }'
