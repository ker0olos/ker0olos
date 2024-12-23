#!/bin/python3

import os
import re
import sys
import time
import asyncio
import datetime

import chat.twitch as twitch
import chat.youtube as youtube
from chat import Message, plays, on_plays
from emoji import demojize

heatmap = {}

t = time.time()

CTRL = False
SHIFT = False

if len(sys.argv) < 2:
    raise Exception("No streaming service was selected")

SERVICE = sys.argv[1]
COMMAND = sys.argv[2] if len(sys.argv) > 2 else None


def on_message(message: Message):
    # clear additional whitespace
    message.text = re.sub(r"\s+", " ", message.text).strip()

    match COMMAND:
        # keeps track of the most sent words since the process started
        case "votes":
            # split the message to a list of unique case-insensitive words
            # then add add to words to a heatmap
            for w in set(
                re.findall(
                    "[a-zA-Z-]+", re.sub(r":.*:", "", demojize(message.text).lower())
                )
            ):
                if len(w) > 0:
                    # length = max(message.bits * 0.5, 1)
                    # if w not in heatmap:
                    #     heatmap[w] = length
                    # else:
                    heatmap[w] += max(message.bits * 0.5, 1)

        # chat plays mode
        case "plays":
            on_plays(message)

        # print all incoming messages in order
        case _:
            print(f"\n[{message.bits}][{message.author}]: {message.text}")


async def main():
    try:
        match SERVICE:
            case "twitch":
                chat = twitch.Chat(os.environ["TWITCH_CHANNEL"])
            case "youtube":
                chat = youtube.Chat(os.environ["YOUTUBE_CHANNEL"])
            case _:
                raise Exception("Unsupported service")

        chat.start()

        chat.listen(on_message)

        print(f"\nConnected to {SERVICE}!\n")

        while True:
            # keeps track of the most sent words since the process started
            # very convenient and plug-less tool for doing chat polls
            if COMMAND == "votes":
                # clear the terminal
                print("\033c", end="")

                # print an x amount of used words in order of most used
                for word in sorted(heatmap, key=heatmap.__getitem__, reverse=True)[:8]:
                    print(f"[{word}]:= {heatmap[word]}")

                # print elapsed time
                print(f"\n{datetime.timedelta(seconds=round(time.time() - t))}")

                time.sleep(1)

    finally:
        plays.stop()
        chat.stop()


if __name__ == "__main__":
    asyncio.run(main())
