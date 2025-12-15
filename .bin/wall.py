#!/Users/ker0olos/bin/venv/bin/python3

import asyncio
import os
import platform
import subprocess
import sys
import urllib
import urllib.request

import aiohttp
import dearpygui.dearpygui as dpg
import praw
from dotenv import load_dotenv
from PIL import Image, ImageFilter

load_dotenv()

dpg.create_context()


_MIN_VOTES = 2
_MIN_WIDTH = 2560
_MIN_HEIGHT = 1440

# Portrait monitor dimensions
_PORTRAIT_WIDTH = 1080
_PORTRAIT_HEIGHT = 1920

# Dual monitor combined dimensions
_DUAL_WIDTH = _PORTRAIT_WIDTH + _MIN_WIDTH
_DUAL_HEIGHT = max(_PORTRAIT_HEIGHT, _MIN_HEIGHT)

_BLACKLIST = ["Naruto", "Evangelion", "Bunny"]

# default subreddit
SUBREDDIT = "Animewallpaper"

REDDIT = praw.Reddit(
    user_agent="wall.py",
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    username=os.environ["REDDIT_USERNAME"],
    password=os.environ["REDDIT_PASSWORD"],
)

_SUBREDDIT = REDDIT.subreddit(SUBREDDIT)

# where to store cached images
_REAL_DIRECTORY = os.path.expanduser("~/Pictures/.wall/")
_CACHE_DIRECTORY = os.path.expanduser("~/Pictures/.wall/_cache/")

os.makedirs(_CACHE_DIRECTORY, exist_ok=True)
os.makedirs(_REAL_DIRECTORY, exist_ok=True)

# exits if the subreddit doesn't exist
try:
    REDDIT.subreddit(SUBREDDIT).id
except Exception:
    print("r/{} is not a valid subreddit".format(_SUBREDDIT))
    sys.exit(1)

# print welcome message


wallpaper_script = wallpaper_script = (
    ["powershell.exe", "-File", "C:\\Users\\kerol\\Documents\\.bin\\wall.ps1"]
    if platform.system() == "Windows"
    else ["wall.sh"]
)


QUERY = ""


_POSTS = (
    _SUBREDDIT.search(query=QUERY, sort="hot", time_filter="year")
    if QUERY
    else _SUBREDDIT.hot(limit=15)
)

images_to_display = []


def resolve_url(post):
    try:
        urls = []
        for [index, media_id] in enumerate(post.media_metadata):
            urls.append(
                dict(
                    id=media_id,
                    url=post.media_metadata[media_id]["s"]["u"],
                    preview=post.preview["images"][index]["source"]["url"],
                )
            )
        return urls
    except Exception:
        if post.url.startswith("https://i.redd.it/") or post.url.startswith(
            "https://i.imgur.com/"
        ):
            return [
                dict(
                    id=post.id,
                    url=post.url,
                    preview=post.preview["images"][0]["source"]["url"],
                )
            ]
        else:
            return []


def process_image(sender, app_data, user_data):
    filename, ext, url, post = user_data
    urllib.request.urlretrieve(url, filename + ext)
    with Image.open(filename + ext) as img:
        resize_image(img, filename)
        wallpaper_path = filename + "_landscape.png"
        
        if platform.system() == "Windows":
            # Use ctypes to set the wallpaper on Windows
            import ctypes

            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDCHANGE = 0x02
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                wallpaper_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
            )
        elif platform.system() == "Darwin":
            # macOS - set wallpaper (macOS will use last saved scaling preference)
            applescript = f'''
            tell application "System Events"
                tell every desktop
                    set picture to "{wallpaper_path}"
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript])
            # Then set to fill screen mode using a separate command
            subprocess.run([
                "osascript", "-e",
                'tell application "System Events" to set picture rotation of current desktop to 0'
            ])
        else:
            # Linux - use the shell script
            subprocess.Popen(
                wallpaper_script
                + [
                    "-u",
                    wallpaper_path,
                    filename + ext,
                ]
            )

    post.upvote()


def create_dual_monitor_wallpaper(sender, app_data, user_data):
    filename, ext, url, post = user_data
    urllib.request.urlretrieve(url, filename + ext)
    with Image.open(filename + ext) as img:
        # Create dual monitor wallpaper - side by side, bottom-aligned
        dual_wallpaper = Image.new(
            "RGBA",
            (_PORTRAIT_WIDTH + _MIN_WIDTH, max(_PORTRAIT_HEIGHT, _MIN_HEIGHT)),
            (0, 0, 0, 255),
        )

        # Create a zoomed and cropped image for portrait monitor (left)
        # Calculate the crop dimensions based on aspect ratio
        img_aspect = img.width / img.height
        port_aspect = _PORTRAIT_WIDTH / _PORTRAIT_HEIGHT

        if img_aspect > port_aspect:  # Image is wider than portrait monitor
            # Calculate the width needed to maintain height while matching portrait aspect ratio
            target_width = int(_PORTRAIT_HEIGHT * img_aspect)
            # Resize image to target height while maintaining aspect ratio
            port_img = img.resize(
                (target_width, _PORTRAIT_HEIGHT),
                resample=Image.Resampling.LANCZOS,
            )
            # Crop the center portion to match portrait width
            left_margin = (target_width - _PORTRAIT_WIDTH) // 2
            port_bg = port_img.crop(
                (left_margin, 0, left_margin + _PORTRAIT_WIDTH, _PORTRAIT_HEIGHT)
            )
        else:  # Image is taller than portrait monitor
            # Calculate the height needed to maintain width while matching portrait aspect ratio
            target_height = int(_PORTRAIT_WIDTH / img_aspect)
            # Resize image to target width while maintaining aspect ratio
            port_img = img.resize(
                (_PORTRAIT_WIDTH, target_height),
                resample=Image.Resampling.LANCZOS,
            )
            # Crop the center portion to match portrait height
            top_margin = (target_height - _PORTRAIT_HEIGHT) // 2
            port_bg = port_img.crop(
                (0, top_margin, _PORTRAIT_WIDTH, top_margin + _PORTRAIT_HEIGHT)
            )

        port_bg = port_bg.convert("RGBA")

        # Create landscape image for second monitor (right)
        landscape_ratio = _MIN_HEIGHT / img.size[1]
        landscape_size = (int(img.size[0] * landscape_ratio), _MIN_HEIGHT)
        landscape_img = img.resize(
            size=landscape_size, resample=Image.Resampling.LANCZOS
        )

        # Create landscape background for landscape monitor
        land_bg = img.resize(
            size=(_MIN_WIDTH, _MIN_HEIGHT), resample=Image.Resampling.LANCZOS
        )
        land_bg = land_bg.convert("RGBA")
        land_bg = land_bg.filter(ImageFilter.GaussianBlur(radius=25))
        land_bg.paste(
            landscape_img, box=(int((_MIN_WIDTH - landscape_size[0]) * 0.5), 0)
        )

        # Calculate vertical offset to bottom-align the monitors
        # Portrait monitor is taller, so landscape needs to be positioned with an offset
        vertical_offset = _PORTRAIT_HEIGHT - _MIN_HEIGHT

        # Combine the two images side by side, bottom-aligned
        dual_wallpaper.paste(port_bg, (0, 0))  # Portrait at left
        dual_wallpaper.paste(
            land_bg, (_PORTRAIT_WIDTH, vertical_offset)
        )  # Landscape at right, bottom-aligned

        # Save the dual monitor wallpaper
        dual_wallpaper_path = filename + "_dual.png"
        dual_wallpaper.save(fp=dual_wallpaper_path, format="png")

        if platform.system() == "Windows":
            import ctypes

            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDCHANGE = 0x02
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                dual_wallpaper_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
            )
        elif platform.system() == "Darwin":
            # macOS - set wallpaper (macOS will use last saved scaling preference)
            applescript = f'''
            tell application "System Events"
                tell every desktop
                    set picture to "{dual_wallpaper_path}"
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript])
            # Then set to fill screen mode using a separate command
            subprocess.run([
                "osascript", "-e",
                'tell application "System Events" to set picture rotation of current desktop to 0'
            ])
        else:
            # Linux - use the shell script
            subprocess.Popen(
                wallpaper_script
                + [
                    "-u",
                    dual_wallpaper_path,
                    filename + ext,
                ]
            )

    post.upvote()


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


for post_index, post in enumerate(_POSTS):
    # skip posts with unconvincing number of up votes
    if post.score < _MIN_VOTES:
        continue

    # resolve all the urls in the post
    data = resolve_url(post)

    for i, obj in enumerate(data):
        [item_id, url, preview] = obj.values()

        path = urllib.parse.urlparse(url).path
        ext = os.path.splitext(path)[1]

        filename = os.path.join(_REAL_DIRECTORY, item_id)

        # skip blacklisted terms
        if any(s in post.title for s in _BLACKLIST):
            continue

        images_to_display.append((item_id, post, preview, url, filename, ext))

        async def download_image(url, filename, ext):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open(filename + ext, "wb") as f:
                            f.write(await resp.read())

        async def main():
            tasks = []

            for i in images_to_display:
                item_id, post, preview, url, filename, ext = i
                # print(preview)
                cached_filename = os.path.join(_CACHE_DIRECTORY, item_id)
                task = asyncio.create_task(
                    download_image(preview, cached_filename, ext)
                )
                tasks.append(task)

            await asyncio.gather(*tasks)

        asyncio.run(main())


with dpg.window(tag="wall.py"):
    # Create a table with 3 columns for the grid layout
    with dpg.table(
        header_row=False,
        borders_innerH=False,
        borders_outerH=False,
        borders_innerV=False,
        borders_outerV=False,
        policy=dpg.mvTable_SizingFixedFit,
    ):
        # Define 3 columns with equal width
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()

        # Display images in rows with 3 columns each
        for i in range(0, len(images_to_display), 3):
            with dpg.table_row():
                # Add up to 3 images in this row
                for j in range(3):
                    if i + j < len(images_to_display):
                        item_id, post, preview, url, filename, ext = images_to_display[
                            i + j
                        ]

                        cached_filename = os.path.join(_CACHE_DIRECTORY, item_id)

                        with dpg.table_cell():
                            # Load and display image
                            width, height, _, data = dpg.load_image(
                                cached_filename + ext
                            )

                            preview_width = 300
                            aspect_ratio = height / width
                            preview_height = int(preview_width * aspect_ratio)

                            with dpg.texture_registry():
                                dpg.add_static_texture(
                                    width=width,
                                    height=height,
                                    default_value=data,
                                    tag=item_id,
                                )

                            with dpg.group():
                                dpg.add_image(
                                    texture_tag=item_id,
                                    width=preview_width,
                                    height=preview_height,
                                )
                                with dpg.group(horizontal=True):
                                    dpg.add_button(
                                        label="Set as Wallpaper",
                                        callback=process_image,
                                        user_data=(filename, ext, url, post),
                                        width=150,
                                    )
                                    dpg.add_button(
                                        label="Set as Dual Monitor",
                                        callback=create_dual_monitor_wallpaper,
                                        user_data=(filename, ext, url, post),
                                        width=150,
                                    )

dpg.create_viewport(title="wall.py")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("wall.py", True)
dpg.start_dearpygui()
dpg.destroy_context()
