#!/usr/bin/python

import re
import os
import sys
import signal
import socket

from pynput import keyboard

from emoji import demojize

PORT = 6667
NICKNAME = "*"
CHANNEL = "#%s" % os.environ["TWITCH_CHANNEL"]
TOKEN = os.environ["TWITCH_TOKEN"]
SERVER = "irc.chat.twitch.tv"

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

try:
    keyboard.Listener(on_press=on_press, on_release=on_release).start()

    while True:
        resp = sock.recv(1024 * 4).decode("utf-8")

        if resp.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))

        matches = re.search(
            ":(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)", demojize(resp)
        )

        if not matches:
            print(resp)
            continue

        username, _, message = matches.groups()

        if COMMAND == "chat":
            print(f"\n[{username}]: {message}")
        else:
            raise Exception("Unsupported command")

except KeyboardInterrupt:
    print("Interrupted")
    socket.close()

except Exception as e:
    print("Exception:", e)
    raise e
