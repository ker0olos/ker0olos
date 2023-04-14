#!/usr/bin/python

# TODO somehow find a way to bookmark photos automatically

import os
import subprocess
import sys
import urllib

import praw
from PIL import Image, ImageFilter

_MIN_VOTES = 50
_MIN_WIDTH = 1366
_MIN_HEIGHT = 768

_BLACKLIST = ["Naruto", "Evangelion", "Bunny"]

# default subreddit
SUBREDDIT = "Animewallpaper"

# search query
QUERY = ""

REDDIT = praw.Reddit(
    user_agent="wall.py",
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    username=os.environ["REDDIT_USERNAME"],
    password=os.environ["REDDIT_PASSWORD"],
)

# check if a subreddit and/or a search query are specified
try:
    QUERY = sys.argv[1] if sys.argv[1] != "-l" else None
except Exception:
    pass

_SUBREDDIT = REDDIT.subreddit(SUBREDDIT)

# where to store cached images
_CACHE_DIRECTORY = os.path.expanduser("~/Pictures/.wall/")

x = "8"
y = "50"
width = "450"
height = "150"
subprocess.Popen(["bspc", "node", "focused", "-t", "floating"])
subprocess.Popen(
    ["xdotool", "getactivewindow", "windowsize", width, height, "windowmove", x, y]
)

# exits if the subreddit doesn't exist
try:
    REDDIT.subreddit(SUBREDDIT).id
except Exception:
    print("r/{} is not a valid subreddit".format(_SUBREDDIT))
    sys.exit(1)

# print welcome message

print("\n--------------------------------------------")
print(("r/{} ~ {}" if QUERY else "r/{}").format(SUBREDDIT, QUERY))
print("--------------------------------------------\n")


def resolve_url(post):
    try:
        urls = []
        for media_id in post.media_metadata:
            urls.append(dict(id=media_id, url=post.media_metadata[media_id]["s"]["u"]))
        return urls
    except Exception:
        if post.url.startswith("https://i.redd.it/") or post.url.startswith(
            "https://i.imgur.com/"
        ):
            return [dict(id=post.id, url=post.url)]
        else:
            return []


def process_image(title, length, index, filename, ext, url):
    if not os.path.isfile(filename + ext):
        urllib.request.urlretrieve(url, filename + ext)

    print("\n" + title + "\n")

    CHOICES = "(f)orward"

    if index > 0:
        CHOICES += "/(p)revious"

    if length > 1:
        CHOICES += "/(s)skip"

    CHOICES += "/(q)uit"

    # notify user about how many images are left in the collection
    if length > 1:
        print(" {} left in this collection.".format(length))

    with Image.open(filename + ext) as img:
        # image is in portrait
        if img.size[0] < img.size[1]:
            if "-l" not in sys.argv:
                resize_image(img, filename)
                subprocess.Popen(
                    ["wall.sh", "-u", filename + "_landscape.png", filename + ext]
                )
                return input(f"Do you want to keep going? {CHOICES}: ")
            else:
                return "f"
        # image is in landscape
        else:
            subprocess.Popen(["wall.sh", "-u", filename + ext])
            return input(f"Do you want to keep going? {CHOICES}: ")


def resize_image(img, filename):
    ratio = _MIN_HEIGHT / img.size[1]

    copy_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
    copy_postion = (int((_MIN_WIDTH * 0.5) - (copy_size[0] * 0.5)), 0)

    # resize the image to fit the desired size with while keeping its aspect ratio
    copy = img.resize(size=copy_size, resample=Image.Resampling.LANCZOS)

    # resize the image to stretch to the desired size
    background_copy = img.resize(
        size=(_MIN_WIDTH, _MIN_HEIGHT), resample=Image.Resampling.LANCZOS
    )

    background_copy = background_copy.convert("RGBA")

    # blur the background copy of the image
    background_copy = background_copy.filter(ImageFilter.GaussianBlur(radius=25))

    # center the rotated image inside the background
    # background_copy.alpha_composite(copy, dest=copy_postion)
    background_copy.paste(copy, box=copy_postion)

    # save the new one image
    background_copy.save(fp=filename + "_landscape.png", format="png")


INDEX = 0

HISTORY = []


_POSTS = (
    _SUBREDDIT.search(query=QUERY, sort="hot", time_filter="year")
    if QUERY
    else _SUBREDDIT.hot(limit=20)
)

for post_index, post in enumerate(_POSTS):
    # skip posts with unconvincing number of up votes
    if post.score < _MIN_VOTES:
        # print('  - {} is not enough up votes.'.format(post.score))
        continue

    # resolve all the urls in the post
    # returns a list of ids and urls
    data = resolve_url(post)

    for i, obj in enumerate(data):
        [item_id, url] = obj.values()

        path = urllib.parse.urlparse(url).path
        ext = os.path.splitext(path)[1]

        filename = os.path.join(_CACHE_DIRECTORY, item_id)

        # skip blacklisted terms
        if any(s in post.title for s in _BLACKLIST):
            continue

        # skip used images
        if os.path.isfile(filename + ext):
            # print('  - already used before')
            continue

        user_input = process_image(
            post.title, len(data) - 1 - i, INDEX, filename, ext, url
        )

        HISTORY.append((post.title, filename, ext))

        # skip the collection
        if user_input.lower() == "s":
            break

        # quit the script
        if user_input.lower() == "f":
            INDEX += 1
        # go back to the previous image
        elif user_input.lower() == "p" and INDEX > 0:
            INDEX -= 1

            while INDEX < len(HISTORY):
                user_input = process_image(
                    HISTORY[INDEX][0],
                    0,
                    INDEX,
                    HISTORY[INDEX][1],
                    HISTORY[INDEX][2],
                    None,
                )

                if user_input.lower() == "f":
                    INDEX += 1
                elif user_input.lower() == "p" and INDEX > 0:
                    INDEX -= 1
                else:
                    print(url)
                    post.upvote()
                    sys.exit()
        else:
            print(url)
            post.upvote()
            sys.exit()
