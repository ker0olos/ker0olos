#!/usr/bin/python

# Original script by mrsorensen
# https://github.com/mrsorensen/reddit-wallpaper-downloader/blob/013d075fc7c1b51e1ecbaf0908ab66cbe0db9b45/getWalls.py

# ---------------------
# USER CONFIG ---------
# ---------------------

# Where to store cached images
cache_directory = '~/Pictures/.wall/'
# default subreddit to download from
subreddit = 'Animewallpaper'
# search query
query = ''
# minimal up votes
up_votes=50
# min_width = 1920
# min_height = 1080
min_width = 1366
min_height = 768
# How many posts to get for each request (max=100)
limit = 100
# Increase this number if the number above limit is not enough posts
pages = 5

# ---------------------
# IMPORTS -------------
# ---------------------
import os
from os.path import expanduser
import sys
import requests
import urllib
import subprocess
from PIL import Image, ImageFilter

# Returns false on status code error
def validURL(URL):
  statusCode = requests.get(URL, headers = {'User-agent':'getWallpapers'}).status_code
  if statusCode == 404:
    return False
  else:
    return True

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
  else:
    return False

# Returns true if image from URL is already used
def alreadySeen(URL):
  imgName = os.path.basename(URL)
  localFilePath = os.path.join(cache_directory, imgName)

  if os.path.isfile(localFilePath):
    return True
  else:
    return False

# Returns false if image from post/URL is not from reddit or imgur domain
def knownURL(post):
  if post.lower().startswith('https://i.redd.it/') or post.lower().startswith('http://i.redd.it/') or post.lower().startswith('https://i.imgur.com/') or post.lower().startswith('http://i.imgur.com/'):
    return True
  else:
    return False

def processImage(post, filename):
  urllib.request.urlretrieve(post, filename)

  with Image.open(filename) as img:
    # Image is in protrait
    if img.size[0] < img.size[1]:
      resizeImage(img, filename)
  
  subprocess.Popen(['wall.sh', '-u', filename ])

def resizeImage(img, filename):
  ratio = min_height / img.size[1]

  copy_size=(int(img.size[0] * ratio), int(img.size[1] * ratio))
  copy_postion=(int((min_width * 0.5) - (copy_size[0] * 0.5)), 0)

  # resize the image to fit the desired size with while keeping its aspect ratio
  copy = img.resize(size=copy_size, resample=Image.ANTIALIAS)
  
  # resize the image to stretch to the desired size
  background_copy = img.resize(size=(min_width, min_height), resample=Image.ANTIALIAS)

  # blur the background copy of the image
  background_copy = background_copy.filter(ImageFilter.GaussianBlur(radius=25))

  # rotate the original image
  # FIXME resampling looks like shit
  # copy = copy.convert('RGBA').rotate(angle=5, resample=Image.NEAREST, expand=1)

  # center the rotated image inside the background
  # background_copy.alpha_composite(copy, dest=copy_postion)
  background_copy.paste(copy, box=copy_postion)
  
  # override the original image with the new one
  background_copy.save(fp=filename)

# ---------------------
# START SCRIPT --------
# ---------------------

# Check if a subreddit and/or a search query are specified
try:
  subreddit = sys.argv[1]
  query     = sys.argv[2]
except:
  pass

cache_directory = expanduser(cache_directory)

# Exits if invalid subreddit name
if not verifySubreddit(subreddit):
  print('r/{} is not a valid subreddit'.format(subreddit))
  sys.exit()

# Print starting message

print('\n--------------------------------------------')
if query:
  print('{} at r/{}'.format(query, subreddit))
else:
  print('r/{}'.format(subreddit))
print('--------------------------------------------\n')

i = 0
after = ''

while i < pages:
  if query:
    # https://www.reddit.com/dev/api/#GET_search
    URL = 'https://reddit.com/r/{}/search/.json?q={}&t=week&sort=top&limit={}&after={}'.format(subreddit, query, limit, after)
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
    if post['data']['ups'] < up_votes:
      print('  Skipping: {} is not enough up votes.'.format(post['data']['ups']))
      continue

    # if post['data']['link_flair_text'] and post['data']['link_flair_text'] != 'Desktop':
    #   print('  Skipping: post is not for landscape. {}.'.format(post['data']['link_flair_text']))
    #   continue
    
    # Shortening variable name
    post = post['data']['url']

    # Skip already used images
    if alreadySeen(post):
      # print('  Skipping: already seen image')
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

    else:
      # update current wallpaper with the new one
      processImage(post, os.path.join(cache_directory, os.path.basename(post)))
      sys.exit(0)
