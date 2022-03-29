#!/usr/bin/python

import os
import re
import sys
import time
import signal
import datetime
import subprocess

from emoji import demojize
from pynput import mouse, keyboard

import yt
import twitch

heatmap = {}

t = time.time()

CTRL = False
SHIFT = False

if len(sys.argv) < 2:
    raise Exception("No streaming service was selected")

SERVICE = sys.argv[1]
COMMAND = sys.argv[2] if len(sys.argv) > 2 else None

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()


def on_keydown(key):
    global CTRL
    global SHIFT

    if key == keyboard.Key.ctrl:
        CTRL = True
    elif key == keyboard.Key.shift:
        SHIFT = True


def on_keyup(key):
    global CTRL
    global SHIFT

    if key == keyboard.Key.ctrl:
        CTRL = False
    elif key == keyboard.Key.shift:
        SHIFT = False
    elif key == keyboard.Key.esc and SHIFT and CTRL:
        os.kill(os.getpid(), signal.SIGINT)


def on_plays(message: twitch.Message):
    mouse_delta = 50

    # trunk-ignore(flake8/E999)
    match message.text:
        case "left":
            mouse_controller.move(dx=mouse_delta, dy=0)
        case "right":
            mouse_controller.move(dx=-mouse_delta, dy=0)

        case "up":
            mouse_controller.move(dx=0, dy=-mouse_delta)
        case "down":
            mouse_controller.move(dx=0, dy=mouse_delta)

        case "screenshot":
            subprocess.Popen(["screenshot-full.sh"])

        case "click":
            mouse_controller.click(mouse.Button.left)


def on_message(message: twitch.Message):
    # clear additional whitespace
    message.text = re.sub(r"\s+", " ", message.text).strip()

    # keeps track of the most sent words since the process started
    if COMMAND == "votes":
        # split the message to a list of unique case-insensitive words
        # then add add to words to a heatmap
        for w in set(demojize(re.sub(r":.*:", "", message.text)).lower().split(" ")):
            if len(w) > 0:
                heatmap[w] = 1 if w not in heatmap else heatmap[w] + 1

    elif COMMAND == "plays":
        on_plays(message)

    # print all incoming messages in order
    else:
        print(f"\n[{message.bits}][{message.author}]: {message.text}")


try:
    if SERVICE == "yt":
        chat = yt.Chat(os.environ["YOUTUBE_CHANNEL"])
    elif SERVICE == "twitch":
        chat = twitch.Chat(os.environ["TWITCH_CHANNEL"])
    else:
        raise Exception("Unsupported service")

    keyboard.Listener(on_press=on_keydown, on_release=on_keyup).start()

    chat.start()

    chat.listen(on_message)

    print(f"\nConnected to {SERVICE}! In {COMMAND} mode! \n")

    while True:
        # keeps track of the most sent words since the process started
        # very convenient and plug-less tool for doing chat polls
        if COMMAND == "votes":
            # clear the terminal
            print("\033c", end="")

            # print an x amount of used words in order of most used
            for word in sorted(heatmap, key=heatmap.__getitem__, reverse=True)[:8]:
                print(f"[{word}]:= {heatmap[word]}")

            # print elapsed time
            print(f"\n{datetime.timedelta(seconds=round(time.time() - t))}")

            time.sleep(1)

except KeyboardInterrupt:
    print("terminated\n")

except Exception as e:
    raise e

finally:
    chat.stop()
