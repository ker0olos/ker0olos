import os
import time
import random
import asyncio
import subprocess

from evdev import UInput, AbsInfo
from evdev import ecodes as e

from .twitch import Message

ui = UInput(
    {
        e.EV_KEY: [
            e.BTN_TRIGGER,
            e.BTN_THUMB,
            e.BTN_THUMB2,
            e.BTN_TOP,
            e.BTN_TOP2,
            e.BTN_PINKIE,
            e.BTN_BASE,
            e.BTN_BASE2,
            e.BTN_BASE3,
            e.BTN_BASE4,
            e.BTN_BASE5,
            e.BTN_BASE6,
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
    "x": (e.EV_KEY, e.BTN_TRIGGER, 1),
    "y": (e.EV_KEY, e.BTN_THUMB, 1),
    "a": (e.EV_KEY, e.BTN_THUMB2, 1),
    "b": (e.EV_KEY, e.BTN_TOP, 1),
    # Triggers
    "lb": (
        e.EV_KEY,
        e.BTN_TOP2,
        1,
    ),
    "lt": (e.EV_KEY, e.BTN_PINKIE, 1),
    "rb": (e.EV_KEY, e.BTN_BASE, 1),
    "rt": (e.EV_KEY, e.BTN_BASE2, 1),
    # Menu-Pad
    # "start": e.BTN_BASE3,
    # "select": e.BTN_BASE3,
    # Stick Triggers
    # "l3":e.BTN_BASE5,
    # "r3": e.BTN_BASE6,
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
