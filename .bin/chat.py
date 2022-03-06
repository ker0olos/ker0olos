#!/usr/bin/pypy3

import datetime
import os
import re
import signal
import sys
import time

from emoji import demojize
from pynput import keyboard

from twitch import TwitchChat, TwitchMessage

TOKEN = os.environ["TWITCH_TOKEN"]
CHANNEL = os.environ["TWITCH_CHANNEL"]

heatmap = {}

t = time.time()

CTRL = False
SHIFT = False

COMMAND = sys.argv[1] if len(sys.argv) > 1 else None


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


def on_message(message: TwitchMessage):
    # clear unicode emojis
    message.content = demojize(message.content)

    # clear additional whitespace
    message.content = re.sub("\s+", " ", message.content).strip()

    # keeps track of the most sent words since the process started
    if COMMAND == "votes":
        # split the message to a list of unique case-insensitive words
        # then add add to words to a heatmap
        for word in set(message.content.lower().split(" ")):
            heatmap[word] = 1 if word not in heatmap else heatmap[word] + 1

    # print all incoming messages in order
    else:
        print(f"\n[{message.username}]: {message.content}")


try:
    twitch = TwitchChat(TOKEN, CHANNEL)

    keyboard.Listener(on_press=on_keydown, on_release=on_keyup).start()

    twitch.start()

    twitch.subscribe_chat_message(on_message)

    print(f"\nConnected to {CHANNEL}!\n")

    while not twitch.is_closed:
        # keeps track of the most sent words since the process started
        # very convenient and plug-less tool for doing chat polls
        if COMMAND == "votes":
            # clear the terminal
            print("\033c", end="")

            # print the 8 top used words
            for word in sorted(heatmap, key=heatmap.__getitem__, reverse=True)[:8]:
                print(f"[{word}]:= {heatmap[word]}")

            # print the elapsed time
            print(f"\n{datetime.timedelta(seconds=round(time.time() - t))}")

            time.sleep(1)

except KeyboardInterrupt:
    print("\n\nInterrupted\n")

except Exception as e:
    raise e

finally:
    twitch.stop()
