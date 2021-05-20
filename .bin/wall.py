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
# search query
query = ''
# min_width = 1920
# min_height = 1080
min_width = 1366
min_height = 768
# How many posts to get for each request (max=100)
limit = 100
# Increase this number if the number above limit is not enough posts
loops = 5

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

# Check if a subreddit and/or a search query are specified
try:
  subreddit = sys.argv[1]
  query     = sys.argv[2]
except:
  pass

directory = expanduser(directory)

# Exits if invalid subreddit name
if not verifySubreddit(subreddit):
  print('r/{} is not a valid subreddit'.format(subreddit))
  sys.exit()

# Print starting message

print('\n--------------------------------------------')
if query:
  print('r/{} ({}) ({}x{})'.format(subreddit, query, str(min_width), str(min_height)))
else:
  print('r/{} ({}x{})'.format(subreddit, str(min_width), str(min_height)))
print('--------------------------------------------\n')

i = 0
after = ''

while i < loops:
  if query:
    # https://www.reddit.com/dev/api/#GET_search
    URL = 'https://reddit.com/r/{}/search/.json?q={}&t=all&sort=hot&limit={}&after={}'.format(subreddit, query, limit, after)
  else:
    # https://www.reddit.com/dev/api/#GET_hot
    URL = 'https://reddit.com/r/{}/hot/.json?limit={}&after={}'.format(subreddit, limit, after)
  
  data = requests.get(URL, headers = {'user-agent':'wall.py'}).json()['data']

  i += 1
  after = data['after']

  # Loops through all posts
  for post in data['children']:
    # print the post's title
    print(post['data']['title'])

    # Skip post with unconvincing up votes
    if post['data']['ups'] < 50:
      print('  Skipping: {} is not enough up votes.'.format(post['data']['ups']))
      continue

    # if post['data']['link_flair_text'] and post['data']['link_flair_text'] != 'Desktop':
    #   print('  Skipping: post is not for landscape. {}.'.format(post['data']['link_flair_text']))
    #   continue
    
    # Shortening variable name
    post = post['data']['url']

    # Skip already downloaded images
    if alreadyDownloaded(post):
      print('  Skipping: already used image')
      continue

    # Skip unknown URLs
    elif not knownURL(post):
      print('  Skipping: unhandled url')
      continue

    # Skip post if not image
    elif not isImg(post):
      print('  Skipping: no image in this post')
      continue

    # Skip post on 404 error
    elif not validURL(post):
      print('  Skipping: invalid url')
      continue

    # Skip post should be HD and landscape
    elif not isFit(post, min_width, min_height):
      print('  Skipping: low resolution or portrait image')
      continue

    # All checks cleared, download image
    else:
      # Store image from post locally
      if storeImg(post):
        # update current wallpaper with the new one
        subprocess.Popen(['wall.sh', '-u', os.path.join(directory, os.path.basename(post))])
        sys.exit(0)
      # For unexpected errors
      else:
        print('  Skipping: unexpected error')
