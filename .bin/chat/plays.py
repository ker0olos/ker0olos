# import os
# import time
# import random
# import asyncio
# import subprocess

# import uinput
import evdev
from evdev import UInput, AbsInfo, InputEvent
from evdev import ecodes as e

from .twitch import Message

# https://www.kernel.org/doc/html/v5.17/input/gamepad.html
# bts = {
#     # D-pad
#     # "d-left": uinput.BTN_DPAD_LEFT,
#     # "d-right": uinput.BTN_DPAD_RIGHT,
#     # "d-up": uinput.BTN_DPAD_UP,
#     # "d-down": uinput.BTN_DPAD_DOWN,
#     # Action-pad
#     "x": uinput.BTN_X,
#     "y": uinput.BTN_Y,
#     "a": uinput.BTN_A,
#     "b": uinput.BTN_B,
#     # Triggers
#     # "lb": uinput.BTN_TL,
#     # "lt": uinput.BTN_TL2,
#     # "rb": uinput.BTN_TR,
#     # "rt": uinput.BTN_TL2,
#     # Menu-Pad
#     # "start": uinput.BTN_START,
#     # "select": uinput.BTN_SELECT,
# }

# devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# print(len(devices))
# for device in devices:
#     print(device.path, device.name, device.phys)

# device = evdev.InputDevice("/dev/input/event17")

# print(device.capabilities(verbose=False))

cap = {
    # e.EV_SYN: [e.SYN_REPORT, e.SYN_CONFIG, e.SYN_DROPPED, 4, 21],
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
        (e.ABS_HAT0X, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
        (e.ABS_HAT0Y, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
    ],
    #     4: [4],
    #     21: [80, 81, 88, 89, 90, 96],
}

ui = UInput(cap, name="Chat Plays Virtual Joystick", version=1)

# def probably(chance):
#     return random.random() < chance


# def execute(*command):
#     subprocess.Popen(command, cwd=os.getcwd())


# def invert_screen(timeout):
#     execute("xrandr", "--output", "eDP-1-1", "--rotate", "inverted")
#     time.sleep(timeout)
#     execute("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def stop():
    # execute("xrandr", "--output", "eDP-1-1", "--rotate", "normal")
    # device.destroy()
    ui.close()


def on_plays(message: Message):
    # msg = message.text.lower()

    # Action-pad
    # ui.write(e.EV_KEY, e.BTN_TRIGGER, 1)
    # ui.write(e.EV_KEY, e.BTN_TRIGGER, 0)

    # ui.write(e.EV_KEY, e.BTN_THUMB, 1)
    # ui.write(e.EV_KEY, e.BTN_THUMB2, 1)
    # ui.write(e.EV_KEY, e.BTN_TOP, 1)

    # # Triggers
    # ui.write(e.EV_KEY, e.BTN_TOP2, 1)
    # ui.write(e.EV_KEY, e.BTN_PINKIE, 1)
    # ui.write(e.EV_KEY, e.BTN_BASE, 1)
    # ui.write(e.EV_KEY, e.BTN_BASE2, 1)

    # # Mode Buttons
    # ui.write(e.EV_KEY, e.BTN_BASE3, 1)
    # ui.write(e.EV_KEY, e.BTN_BASE4, 1)

    # # Stick Triggers
    # ui.write(e.EV_KEY, e.BTN_BASE5, 1)
    # ui.write(e.EV_KEY, e.BTN_BASE6, 1)

    # ui.write(e.EV_ABS, e.ABS_X, 1)
    # ui.write(e.EV_ABS, e.ABS_X, 0)
    # ui.write(e.EV_ABS, e.ABS_RX, 1)
    # ui.write(e.EV_ABS, e.ABS_RX, 0)
    ui.write(e.EV_ABS, e.ABS_HAT0X, 1)
    ui.write(e.EV_ABS, e.ABS_HAT0X, 0)
    # ui.write(e.EV_ABS, e.ABS_X, 0)
    # ui.write(e.EV_ABS, e.ABS_Y, 1)
    # ui.write(e.EV_ABS, e.ABS_RX, 1)
    # ui.write(e.EV_ABS, e.ABS_RY, 1)
    # ui.write(e.EV_ABS, e.BTN_BASE6, 1)

    ui.syn()

    # if msg in bts:
    #     print(f"{message.author} -> {msg}")
    #     device.emit_click(uinput.BTN_A)

    # elif msg == "left":
    #     print("left")
    #     device.emit(uinput.ABS_X, 1000000)
    # elif msg == "right":
    #     print("right")
    #     device.emit(uinput.ABS_X, 1000000)
    # device.emit_click(uinput.BTN_RIGHT)
    # device.emit(uinput.ABS_X, 5)
    # elif msg == "up":
    #     device.emit(uinput.ABS_X, 5, syn=False)
    #     device.emit(uinput.ABS_Y, 5)
    # elif msg == "down":
    #     device.emit(uinput.ABS_X, 5, syn=False)
    #     device.emit(uinput.ABS_Y, 5)

    # elif msg == "screenshot":
    #     execute("screenshot-full.sh")

    # elif msg == "invert":
    #     if probably(15 / 100):
    #         asyncio.get_event_loop().run_in_executor(None, invert_screen, 30)

    # else:
    #     return False

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
