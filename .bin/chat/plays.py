import os
import time
import random
import asyncio
import subprocess

from .twitch import Message

arrows = ["Left", "Right", "Up", "Down"]


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


def press(name):
    popen("xdotool", "key", name)


# def repeat(name, times=2):
#     popen("xdotool", "key", "--repeat", str(times), name)


def invert_screen():
    popen("xrandr", "--output", "eDP-1-1", "--rotate", "inverted")
    time.sleep(10)
    popen("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def stop():
    popen("xrandr", "--output", "eDP-1-1", "--rotate", "normal")


def on_plays(message: Message):
    match message.text.lower():
        case "left":
            press(arrows[0])
        case "right":
            press(arrows[1])

        case "up":
            press(arrows[2])
        case "down":
            press(arrows[3])

        case "a":
            press("a")
        case "s":
            press("s")

        case "x":
            press("x")

        case "e":
            press("e")
        case "d":
            press("d")

        case "screenshot":
            popen("screenshot-full.sh")

        case "flip":
            if probably(35 / 100):
                flip()

        case "invert":
            if probably(15 / 100):
                asyncio.get_event_loop().run_in_executor(None, invert_screen)

        case "enter":
            press("Return")
        case _:
            return False

    return True


# if __name__ == "__main__":
#     import pyttsx3

#     engine = pyttsx3.init()
#     engine.setProperty("rate", 150)
#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[2].id)
#     engine.say("I will speak this text")
#     engine.runAndWait()
