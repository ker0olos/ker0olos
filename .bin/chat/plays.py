import subprocess

from pynput import keyboard

from .twitch import Message

# mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()


def on_plays(message: Message):
    match message.text.lower():
        case "left":
            keyboard_controller.press(keyboard.Key.left)
        case "right":
            keyboard_controller.press(keyboard.Key.right)

        case "up":
            keyboard_controller.press(keyboard.Key.up)
        case "down":
            keyboard_controller.press(keyboard.Key.down)

        case "screenshot":
            subprocess.Popen(["screenshot-full.sh"])

        case "enter":
            keyboard_controller.press(keyboard.Key.enter)
        case _:
            return False

    return True
