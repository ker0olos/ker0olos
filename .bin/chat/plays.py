import os
import time
import random
import asyncio
import subprocess

from evdev import UInput, AbsInfo
from evdev import ecodes as e

from .twitch import Message

# https://www.kernel.org/doc/html/v5.17/input/gamepad.html

ui = UInput(
    {
        e.EV_KEY: [
            e.BTN_A,
            e.BTN_B,
            e.BTN_X,
            e.BTN_Y,
            e.BTN_TL,
            e.BTN_TL2,
            e.BTN_TR,
            e.BTN_TR2,
            e.BTN_SELECT,
            e.BTN_START,
            # e.BTN_THUMBL,
            # e.BTN_THUMBR,
        ],
        e.EV_ABS: [
            (e.ABS_X, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
            (e.ABS_Y, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
            (e.ABS_Z, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
            (e.ABS_RX, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
            (e.ABS_RY, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
            (
                e.ABS_HAT0X,
                AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0),
            ),
            (
                e.ABS_HAT0Y,
                AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0),
            ),
        ],
    },
    name="Chat Plays Virtual Joystick",
    version=1,
)

slay_the_spire = {
    "left": lambda: ui_press(e.EV_ABS, e.ABS_HAT0X, -1),
    "right": lambda: ui_press(e.EV_ABS, e.ABS_HAT0X, 1),
    "up": lambda: ui_press(e.EV_ABS, e.ABS_HAT0Y, -1),
    "down": lambda: ui_press(e.EV_ABS, e.ABS_HAT0Y, 1),
    #
    "a": lambda: ui_press(e.EV_KEY, e.BTN_A, 1),
    "use": lambda: ui_press(e.EV_KEY, e.BTN_A, 1),
    "attack": lambda: ui_press(e.EV_KEY, e.BTN_A, 1),
    #
    "b": lambda: ui_press(e.EV_KEY, e.BTN_B, 1),
    "back": lambda: ui_press(e.EV_KEY, e.BTN_B, 1),
    #
    "x": lambda: ui_press(e.EV_KEY, e.BTN_X, 1),
    "potions": lambda: ui_press(e.EV_KEY, e.BTN_X, 1),
    #
    "y": lambda: ui_press(e.EV_KEY, e.BTN_Y, 1),
    "end": lambda: ui_press(e.EV_KEY, e.BTN_Y, 1),
    #
    "lb": lambda: key_press("d"),
    "deck": lambda: key_press("d"),
    #
    "lt": lambda: key_press("a"),
    "pile": lambda: key_press("a"),
    #
    "rb": lambda: key_press("x"),
    "exhaust": lambda: key_press("x"),
    #
    "rt": lambda: key_press("s"),
    "discard": lambda: key_press("s"),
    #
    "start": lambda: key_press("m"),
    "map": lambda: key_press("m"),
}

bts = slay_the_spire


def probably(chance):
    return random.random() < chance


def execute(*command):
    subprocess.Popen(command, cwd=os.getcwd())


def ui_press(m, ev, v):
    ui.write(m, ev, v)
    ui.write(m, ev, 0)


def key_press(name):
    execute("xdotool", "key", name)


def invert_screen(timeout):
    execute("xrandr", "--output", "eDP-1-1", "--rotate", "inverted")
    time.sleep(timeout)
    execute("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def stop():
    execute("xrandr", "--output", "eDP-1-1", "--rotate", "normal")
    ui.close()


def on_plays(message: Message):
    msg = message.text.lower()

    if msg in bts:
        bts[msg]()

    # elif msg == "screenshot":
    #     execute("screenshot-full.sh")

    elif msg == "invert":
        if probably(15 / 100):
            asyncio.get_event_loop().run_in_executor(None, invert_screen, 30)

    else:
        return False

    ui.syn()

    print(f"{message.author} -> {message.text}")

    return True


# if __name__ == "__main__":
#     import pyttsx3

#     engine = pyttsx3.init()
#     engine.setProperty("rate", 150)
#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[2].id)
#     engine.say("I will speak this text")
#     engine.runAndWait()
