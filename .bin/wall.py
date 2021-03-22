#!/usr/bin/python

# Original script by mrsorensen
# https://github.com/mrsorensen/reddit-wallpaper-downloader/blob/013d075fc7c1b51e1ecbaf0908ab66cbe0db9b45/getWalls.py

# ---------------------
# USER CONFIG ---------
# ---------------------

# Where to store downloaded images
directory = '~/Pictures/Wall/'
# default subreddit to download from
subreddit = 'wallpapers'
# min_width = 1920
# min_height = 1080
min_width = 1366
min_height = 768
# How many posts to get for each request (Max 100)
limit = 50

# ---------------------
# IMPORTS -------------
# ---------------------
import os
from os.path import expanduser
import sys
import requests
import urllib
import subprocess
from PIL import ImageFile

# ---------------------
# FUNCTIONS -----------
# ---------------------

# Returns false on status code error
def validURL(URL):
  statusCode = requests.get(URL, headers = {'User-agent':'getWallpapers'}).status_code
  if statusCode == 404:
    return False
  else: return True

# Returns false if subreddit doesn't exist
def verifySubreddit(subreddit):
  URL = 'https://reddit.com/r/{}.json'.format(subreddit)
  result= requests.get(URL, headers = {'User-agent':'getWallpapers'}).json()
  try:
    result['error']
    return False
  except:
    return True

# Returns list of posts from subreddit as json
def getPosts(subreddit, after):
  allPosts = []
    
  # https://www.reddit.com/dev/api/#GET_hot
  URL = 'https://reddit.com/r/{}/hot/.json?&limit={}&after={}'.format(subreddit, limit, after)

  posts = requests.get(URL, headers = {'User-agent':'getWallpapers'}).json()
  for post in posts['data']['children']:
    allPosts.append(post)
  after = posts['data']['after']
  return allPosts

# Returns false if URL is not an image
def isImg(URL):
  if URL.endswith(('.png', '.jpeg', '.jpg')):
    return True
  else: return False

# Returns false if image from URL is not HD (Specified by min-/max_width)
def isFit(URL, min_width, min_height):
  file = urllib.request.urlopen(URL)
  size = file.headers.get("content-length")
  if size: size = int(size)
  p = ImageFile.Parser()
  while 1:
    data = file.read(1024)
    if not data:
      break
    p.feed(data)
    if p.image:
      # return p.image.size
      if p.image.size[0] >= p.image.size[1] and p.image.size[0] >= min_width and p.image.size[1] >= min_height:
        return True
      return False
  file.close()
  return False

# Returns true if image from URL is already downloaded
def alreadyDownloaded(URL):
  imgName = os.path.basename(URL)
  localFilePath = os.path.join(directory, imgName)
  if(os.path.isfile(localFilePath)):
    return True
  else: return False

# Returns false if image from post/URL is not from reddit or imgur domain
def knownURL(post):
  if post.lower().startswith('https://i.redd.it/') or post.lower().startswith('http://i.redd.it/') or post.lower().startswith('https://i.imgur.com/') or post.lower().startswith('http://i.imgur.com/'):
    return True
  else: return False

# Returns true if image from post/URL is stored locally
def storeImg(post):
  if urllib.request.urlretrieve(post, os.path.join(directory, os.path.basename(post))):
    return True
  else:
    return False

# ---------------------
# START SCRIPT --------
# ---------------------

# Check if subreddit name is specified as parameter
try:
  subreddit = sys.argv[1]
except:
  pass

directory = expanduser(directory)

# Exits if invalid subreddit name
if not verifySubreddit(subreddit):
  print('r/{} is not a valid subreddit'.format(subreddit))
  sys.exit()

# Print starting message

print('\n--------------------------------------------')
print('r/{} ({}x{})'.format(subreddit, str(min_width), str(min_height)))
print('--------------------------------------------\n')

# For reddit pagination (Leave empty)
after = ''

# Stores posts from function
posts = getPosts(subreddit, after)

# For adding index numbers to loop
index = 1

# Counting amount of images downloaded
downloadCount = 0

# Loops through all posts
for post in posts:

  # print the post's title
  print(post['data']['title'])

  # Skip post with less than 10 up votes
  if post['data']['ups'] < 10:
    print('  Skipping: not enough up votes')
    index += 1
    continue

  if post['data']['link_flair_text'] and post['data']['link_flair_text'] != 'Desktop':
    print('  Skipping: flair is not for landscape')
    index += 1
    continue
  
  # Shortening variable name
  post = post['data']['url']

  # Skip post on 404 error
  if not validURL(post):
    print('  Skipping: invalid url')
    index += 1
    continue

  # Skip unknown URLs
  elif not knownURL(post):
    print('  Skipping: unhandled url')
    index += 1
    continue

  # Skip post if not image
  elif not isImg(post):
    print('  Skipping: no image in this post')
    index += 1
    continue

  # Skip already downloaded images
  elif alreadyDownloaded(post):
    print('  Skipping: already used image')
    index += 1
    continue

  # Skip post should be HD and landscape
  elif not isFit(post, min_width, min_height):
    print('  Skipping: low resolution or portrait image')
    index += 1
    continue

  # All checks cleared, download image
  else:
    # Store image from post locally
    if storeImg(post):
      # update current wallpaper with the new one
      subprocess.Popen(['wall.sh', '-u', os.path.join(directory, os.path.basename(post))])
      index += 1
      downloadCount += 1
      break
    # For unexpected errors
    else:
      print('  Skipping: unexpected error')
      index += 1