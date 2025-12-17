#!/usr/bin/env python3

import asyncio
import os
import platform
import random
import subprocess
import sys
import threading
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

# List of subreddits to fetch wallpapers from
SUBREDDITS = ["Animewallpaper", "moescape"]

REDDIT = praw.Reddit(
    user_agent="wall.py",
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    username=os.environ["REDDIT_USERNAME"],
    password=os.environ["REDDIT_PASSWORD"],
)

# where to store cached images
_REAL_DIRECTORY = os.path.expanduser("~/Pictures/.wall/")
_CACHE_DIRECTORY = os.path.expanduser("~/Pictures/.wall/_cache/")

os.makedirs(_CACHE_DIRECTORY, exist_ok=True)
os.makedirs(_REAL_DIRECTORY, exist_ok=True)

# validate subreddits exist
for subreddit_name in SUBREDDITS:
    try:
        REDDIT.subreddit(subreddit_name).id
    except Exception:
        print(f"r/{subreddit_name} is not a valid subreddit")
        sys.exit(1)

# print welcome message


wallpaper_script = wallpaper_script = (
    ["powershell.exe", "-File", "C:\\Users\\kerol\\Documents\\.bin\\wall.ps1"]
    if platform.system() == "Windows"
    else ["wall.sh"]
)


QUERY = ""

# Fetch posts from all subreddits
_POSTS = []
for subreddit_name in SUBREDDITS:
    subreddit = REDDIT.subreddit(subreddit_name)
    if QUERY:
        _POSTS.extend(list(subreddit.search(query=QUERY, sort="hot", time_filter="year", limit=10)))
    else:
        _POSTS.extend(list(subreddit.hot(limit=10)))

# Randomize the order of posts
random.shuffle(_POSTS)

images_to_display = []
all_posts_data = []  # Store all post data for "Load More" functionality


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
            try:
                return [
                    dict(
                        id=post.id,
                        url=post.url,
                        preview=post.preview["images"][0]["source"]["url"],
                    )
                ]
            except Exception:
                return []
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

        all_posts_data.append((item_id, post, preview, url, filename, ext))

# Initially show all images
images_to_display = all_posts_data.copy()


async def download_image(url, filename, ext):
    try:
        # Unescape HTML entities in URL
        url = url.replace('&amp;', '&')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(filename + ext, "wb") as f:
                        f.write(await resp.read())
    except Exception:
        pass


async def download_all_images():
    tasks = []
    for i in images_to_display:
        item_id, post, preview, url, filename, ext = i
        cached_filename = os.path.join(_CACHE_DIRECTORY, item_id)
        task = asyncio.create_task(
            download_image(preview, cached_filename, ext)
        )
        tasks.append(task)
    await asyncio.gather(*tasks)


def load_and_display_images():
    """Load images after they're downloaded and update the UI"""
    # Remove loading indicator
    if dpg.does_item_exist("loading_text"):
        dpg.delete_item("loading_text")
    if dpg.does_item_exist("loading_indicator"):
        dpg.delete_item("loading_indicator")
    
    # Show the scrollable window
    dpg.show_item("scroll_window")
    
    # Display images in rows with 3 columns each
    for i in range(0, len(images_to_display), 3):
        with dpg.table_row(parent="image_table"):
            # Add up to 3 images in this row
            for j in range(3):
                if i + j < len(images_to_display):
                    item_id, post, preview, url, filename, ext = images_to_display[
                        i + j
                    ]

                    cached_filename = os.path.join(_CACHE_DIRECTORY, item_id)

                    with dpg.table_cell():
                        try:
                            # Check if file exists
                            if not os.path.exists(cached_filename + ext):
                                dpg.add_text(f"File not found: {item_id}")
                                continue
                                
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
                                    # Only show dual monitor button on non-macOS systems
                                    if platform.system() != "Darwin":
                                        dpg.add_button(
                                            label="Set as Dual Monitor",
                                            callback=create_dual_monitor_wallpaper,
                                            user_data=(filename, ext, url, post),
                                            width=150,
                                        )
                        except Exception as e:
                            dpg.add_text(f"Failed to load image: {e}")
    
    # Show Load More button
    if dpg.does_item_exist("load_more_container"):
        dpg.show_item("load_more_container")


def load_more_images():
    """Fetch and display more images from subreddits"""
    dpg.hide_item("load_more_button")
    dpg.show_item("load_more_loading")
    
    def fetch_more():
        global _POSTS, all_posts_data, images_to_display
        
        # Fetch more posts from all subreddits
        new_posts = []
        for subreddit_name in SUBREDDITS:
            subreddit = REDDIT.subreddit(subreddit_name)
            if QUERY:
                new_posts.extend(list(subreddit.search(query=QUERY, sort="hot", time_filter="year", limit=10)))
            else:
                # Get next batch of posts
                existing_count = len([p for p in _POSTS if p.subreddit.display_name.lower() == subreddit_name.lower()])
                new_posts.extend(list(subreddit.hot(limit=10 + existing_count))[existing_count:])
        
        # Randomize new posts
        random.shuffle(new_posts)
        _POSTS.extend(new_posts)
        
        # Process new posts
        new_images = []
        for post in new_posts:
            if post.score < _MIN_VOTES:
                continue
            
            data = resolve_url(post)
            for i, obj in enumerate(data):
                [item_id, url, preview] = obj.values()
                path = urllib.parse.urlparse(url).path
                ext = os.path.splitext(path)[1]
                filename = os.path.join(_REAL_DIRECTORY, item_id)
                
                if any(s in post.title for s in _BLACKLIST):
                    continue
                
                new_images.append((item_id, post, preview, url, filename, ext))
        
        all_posts_data.extend(new_images)
        images_to_display.extend(new_images)
        
        # Download new images
        async def download_new_images():
            tasks = []
            for item_id, post, preview, url, filename, ext in new_images:
                cached_filename = os.path.join(_CACHE_DIRECTORY, item_id)
                task = asyncio.create_task(download_image(preview, cached_filename, ext))
                tasks.append(task)
            await asyncio.gather(*tasks)
        
        # Windows fix: Set event loop policy for asyncio in threads
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(download_new_images())
        
        # Display new images
        start_index = len(images_to_display) - len(new_images)
        for i in range(start_index, len(images_to_display), 3):
            with dpg.table_row(parent="image_table"):
                for j in range(3):
                    if i + j < len(images_to_display):
                        item_id, post, preview, url, filename, ext = images_to_display[i + j]
                        cached_filename = os.path.join(_CACHE_DIRECTORY, item_id)
                        
                        with dpg.table_cell():
                            try:
                                width, height, _, data = dpg.load_image(cached_filename + ext)
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
                                        if platform.system() != "Darwin":
                                            dpg.add_button(
                                                label="Set as Dual Monitor",
                                                callback=create_dual_monitor_wallpaper,
                                                user_data=(filename, ext, url, post),
                                                width=150,
                                            )
                            except Exception as e:
                                dpg.add_text(f"Failed to load image: {e}")
        
        # Show button again
        dpg.hide_item("load_more_loading")
        dpg.show_item("load_more_button")
    
    # Run in background thread
    thread = threading.Thread(target=fetch_more, daemon=True)
    thread.start()


def download_images_thread():
    """Run async download in a separate thread"""
    # Windows fix: Set event loop policy for asyncio in threads
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(download_all_images())
    # After download completes, update UI in main thread
    load_and_display_images()


# Create UI window with loading state
with dpg.window(tag="wall.py", width=1000, height=800):
    dpg.add_text("Loading wallpapers...", tag="loading_text")
    dpg.add_loading_indicator(style=1, tag="loading_indicator")
    
    # Create a child window to enable scrolling
    with dpg.child_window(tag="scroll_window", width=-1, height=-1, show=False):
        # Create a table with 3 columns for the grid layout
        with dpg.table(
            tag="image_table",
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
    
        # Load More button container (hidden initially)
        with dpg.group(tag="load_more_container", show=False):
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=350)
                dpg.add_button(
                    label="Load More Wallpapers",
                    callback=load_more_images,
                    tag="load_more_button",
                    width=200,
                    height=40,
                )
                dpg.add_loading_indicator(
                    style=1,
                    tag="load_more_loading",
                    show=False,
                )


dpg.create_viewport(title="wall.py", width=1024, height=768)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("wall.py", True)

# Start downloading images in background thread
thread = threading.Thread(target=download_images_thread, daemon=True)
thread.start()

dpg.start_dearpygui()
dpg.destroy_context()
