#!/bin/bash

MICROPHONE="alsa_input.usb-0c8f_USB_Audio_Device-00.mono-fallback"
SPEAKERS="bluez_sink.7B_F8_19_1B_EC_E1.a2dp_sink"
#SPEAKERS="alsa_output.pci-0000_00_1b.0.analog-stereo"

pactl load-module module-null-sink sink_name=Virtual1
pactl load-module module-loopback source=$MICROPHONE sink=Virtual1
pactl load-module module-loopback source=Virtual1.monitor sink=$SPEAKERS