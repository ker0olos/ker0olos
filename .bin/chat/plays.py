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
            e.BTN_MODE,
            e.BTN_THUMBL,
            e.BTN_THUMBR,
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


bts = {
    # Stick
    "left": (e.EV_ABS, e.ABS_HAT0X, -1),
    "right": (e.EV_ABS, e.ABS_HAT0X, 1),
    "up": (e.EV_ABS, e.ABS_HAT0Y, -1),
    "down": (e.EV_ABS, e.ABS_HAT0Y, 1),
    # Action-pad
    "a": (e.EV_KEY, e.BTN_A, 1),
    "b": (e.EV_KEY, e.BTN_B, 1),
    "x": (e.EV_KEY, e.BTN_X, 1),
    "y": (e.EV_KEY, e.BTN_Y, 1),
    # Triggers
    "lb": (e.EV_KEY, e.BTN_TL, 1),
    "rb": (e.EV_KEY, e.BTN_TR, 1),
    # Menu-Pad
    # "start": (e.EV_KEY, e.BTN_TL2, 1),
    # "select": (e.EV_KEY, e.BTN_TR2, 1),
    # Stick Triggers
    # "l3": (e.EV_KEY, e.BTN_SELECT, 1),
    # "r3": (e.EV_KEY, e.BTN_START, 1),
}


def probably(chance):
    return random.random() < chance


def execute(*command):
    subprocess.Popen(command, cwd=os.getcwd())


def invert_screen(timeout):
    execute("xrandr", "--output", "eDP-1-1", "--rotate", "inverted")
    time.sleep(timeout)
    execute("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def stop():
    execute("xrandr", "--output", "eDP-1-1", "--rotate", "normal")
    ui.close()


def press(ev):
    ui.write(ev[0], ev[1], ev[2])
    ui.write(ev[0], ev[1], 0)
    ui.syn()


def on_plays(message: Message):
    msg = message.text.lower()

    if msg in bts:
        press(bts[msg])

    # elif msg == "screenshot":
    #     execute("screenshot-full.sh")

    elif msg == "invert":
        if probably(15 / 100):
            asyncio.get_event_loop().run_in_executor(None, invert_screen, 30)

    else:
        return False

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
