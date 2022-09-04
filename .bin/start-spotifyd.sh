#!/bin/bash

until spotifyd --no-daemon; do echo "Daemon died. Starting again..."; done