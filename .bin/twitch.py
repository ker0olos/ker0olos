#!/usr/bin/pypy3

import datetime
import os
import re
import signal
import socket
import sys
import time

from emoji import demojize
from pynput import keyboard

PORT = 6667
NICKNAME = "*"
CHANNEL = "#%s" % os.environ["TWITCH_CHANNEL"]
TOKEN = os.environ["TWITCH_TOKEN"]
SERVER = "irc.chat.twitch.tv"


heatmap = {}

t = time.time()

sock = socket.socket()


CTRL = False
SHIFT = False

COMMAND = sys.argv[1] if len(sys.argv) > 1 else "chat"


def on_press(key):
    global CTRL
    global SHIFT

    if key == keyboard.Key.ctrl:
        CTRL = True
    elif key == keyboard.Key.shift:
        SHIFT = True


def on_release(key):
    global CTRL
    global SHIFT

    if key == keyboard.Key.ctrl:
        CTRL = False
    elif key == keyboard.Key.shift:
        SHIFT = False
    elif key == keyboard.Key.esc and SHIFT and CTRL:
        os.kill(os.getpid(), signal.SIGINT)


sock.connect((SERVER, PORT))

sock.send(f"PASS {TOKEN}\n".encode("utf-8"))
sock.send(f"NICK {NICKNAME}\n".encode("utf-8"))
sock.send(f"JOIN {CHANNEL}\n".encode("utf-8"))

print(f"\nConnected to {CHANNEL}!\n")

try:
    keyboard.Listener(on_press=on_press, on_release=on_release).start()

    while True:
        resp = sock.recv(1024 * 4).decode("utf-8")

        if resp.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))

        resp = demojize(resp)

        resp = re.sub("\s+", " ", resp).strip()

        matches = re.search(":(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)", resp)

        if not matches:
            continue

        username, _, message = matches.groups()

        if COMMAND == "chat":
            print(f"\n[{username}]: {message}")
        elif COMMAND == "votes":
            for word in set(message.lower().split(" ")):
                heatmap[word] = heatmap[word] + 1 if word in heatmap else 1

            arr = sorted(heatmap, key=heatmap.__getitem__, reverse=True)

            # clear the terminal
            print("\033c", end="")

            # print the 8 top used words
            for word in arr[:8]:
                print(f"[{word}]:= {heatmap[word]}")

            # print the elapsed time
            print(f"\n{datetime.timedelta(seconds=round(time.time() - t))}")
        else:
            raise Exception("Unsupported command")

except KeyboardInterrupt:
    print("Interrupted")

except Exception as e:
    raise e

finally:
    sock.close()
