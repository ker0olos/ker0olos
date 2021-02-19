#!/usr/bin/python

import sys

args = sys.argv[1].split('\\n');

timestamp = args[0]
summary = args[1]
name = args[2]

with open('/tmp/dunstlog', 'r') as file:
  lines = file.read().splitlines()

with open('/tmp/dunstlog', 'w') as file:
  index = -1

  for i, s in enumerate(lines):
    if s == timestamp and lines[i+3] == summary and lines[i+4] == name:
      index = i
      break
    elif s == timestamp and lines[i+4] == summary and lines[i+5] == name:
      index = i
      break

  if index > -1:
    del lines[index:index+6]
  
  file.write('\n'.join(lines) + '\n')