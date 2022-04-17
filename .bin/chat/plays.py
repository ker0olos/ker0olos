import os
import time
import random
import asyncio
import subprocess

from pynput import keyboard

from .twitch import Message

# mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

arrows = [keyboard.Key.left, keyboard.Key.right, keyboard.Key.up, keyboard.Key.down]


def probably(chance):
    return random.random() < chance


def flip():
    global arrows
    arrows[0], arrows[1] = arrows[1], arrows[0]
    arrows[2], arrows[3] = arrows[3], arrows[2]


# def is_flipped():
#     return arrows[0] is keyboard.Key.right


def popen(*command):
    subprocess.Popen(command, cwd=os.getcwd())


def invert_screen():
    popen("xrandr", "--output", "eDP-1-1", "--rotate", "inverted")
    time.sleep(10)
    popen("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def stop():
    popen("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def on_plays(message: Message):
    match message.text.lower():
        case "left":
            keyboard_controller.press(arrows[0])
        case "right":
            keyboard_controller.press(arrows[1])

        case "up":
            keyboard_controller.press(arrows[2])
        case "down":
            keyboard_controller.press(arrows[3])

        case "screenshot":
            popen("screenshot-full.sh")

        case "flip":
            if probably(35 / 100):
                flip()

        case "invert":
            if probably(15 / 100):
                asyncio.get_running_loop().run_in_executor(None, invert_screen)

        case "enter":
            keyboard_controller.press(keyboard.Key.enter)
        case _:
            return False

    return True
