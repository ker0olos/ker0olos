#!/usr/bin/python

import os
import sys
import urllib
import subprocess

import timg
import praw

from PIL import Image, ImageFilter

renderer = timg.Renderer()

_MIN_VOTES = 50
_MIN_WIDTH = 1366
_MIN_HEIGHT = 768

# default subreddit
_SUBREDDIT = 'Animewallpaper'

_BLACKLIST = [
  "Naruto",
  "Evangelion",
  "Bunny"
]

# search query
_QUERY = ''

reddit = praw.Reddit(
    user_agent="wall.py",
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD']
)

# check if a subreddit and/or a search query are specified
try:
  _SUBREDDIT = sys.argv[1]
  _QUERY     = sys.argv[2]
except:
  pass

# where to store cached images
_cache_directory = os.path.expanduser('~/Pictures/.wall/')

subreddit = reddit.subreddit(_SUBREDDIT)

# exits if the subreddit doesn't exist

try:
  reddit.subreddit(_SUBREDDIT).id
except:
  print('r/{} is not a valid subreddit'.format(subreddit))
  sys.exit(1)

# print welcome message

print('\n--------------------------------------------')
print(('r/{} ~ {}' if _QUERY else 'r/{}').format(_SUBREDDIT, _QUERY))
print('--------------------------------------------\n')

def resolve_url(post):
  try:
    urls = []
    for media_id in post.media_metadata:
      urls.append(dict(id=media_id, url=post.media_metadata[media_id]['s']['u']))
    return urls
  except:
    if post.url.startswith('https://i.redd.it/') or post.url.startswith('https://i.imgur.com/'):
      return [ dict(id=post.id, url=post.url) ]
    else:
      return []

def process_image(url, filename):
  urllib.request.urlretrieve(url, filename)

  with Image.open(filename) as img:
    # image is in protrait
    if img.size[0] < img.size[1]:
      resize_image(img, filename)
      subprocess.Popen(['wall.sh', '-u', filename + '_landscape', '-p', filename ])
    # image is in landscape
    else:
      subprocess.Popen(['wall.sh', '-u', filename ])

def resize_image(img, filename):
  ratio = _MIN_HEIGHT / img.size[1]

  copy_size=(int(img.size[0] * ratio), int(img.size[1] * ratio))
  copy_postion=(int((_MIN_WIDTH * 0.5) - (copy_size[0] * 0.5)), 0)

  # resize the image to fit the desired size with while keeping its aspect ratio
  copy = img.resize(size=copy_size, resample=Image.ANTIALIAS)

  # resize the image to stretch to the desired size
  background_copy = img.resize(size=(_MIN_WIDTH, _MIN_HEIGHT), resample=Image.ANTIALIAS)

  # blur the background copy of the image
  background_copy = background_copy.filter(ImageFilter.GaussianBlur(radius=25))

  # center the rotated image inside the background
  # background_copy.alpha_composite(copy, dest=copy_postion)
  background_copy.paste(copy, box=copy_postion)

  # save the new one image
  background_copy.save(fp=filename + '_landscape', format='png')

for post in subreddit.search(query=_QUERY, sort='hot', time_filter='week') if _QUERY else subreddit.hot(limit=20): # pylint: disable=line-too-long

  # skip posts with unconvincing number of up votes
  if post.score < _MIN_VOTES:
    # print('  - {} is not enough up votes.'.format(post.score))
    continue

  # resolve all the urls in the post
  # returns a list of ids and urls
  data = resolve_url(post)

  for i, obj  in enumerate(data):
    [ item_id, url ] = obj.values()

    filename = os.path.join(_cache_directory, item_id)

    # skip blacklisted terms
    if any(s in post.title for s in _BLACKLIST):
      continue

    # skip used images
    if os.path.isfile(filename):
      # print('  - already used before')
      continue

    print(post.title)
    # print('{}: https://reddit.com{}'.format(post.title, post.permalink))

    # update current wallpaper with the new one
    process_image(url, filename)

    # notify user about how many images are left in the collection
    if len(data) > 1:
      print('  - {} left in this collection.'.format(len(data) - 1 - i))

    renderer.load_image_from_file(filename)
    renderer.resize(50)

    print('')
    renderer.render(timg.Ansi24HblockMethod)

    user_input = input('Do you want to keep going? (y/s/n) ') if len(data) > 1 else input('Do you want to keep going? (y/n) ') # pylint: disable=line-too-long

    # skip the collection
    if user_input.lower() == 's':
      break

    # exit the after finding one wallpaper that can be used
    if user_input.lower() != 'y':
      sys.exit()
    else:
      print('')
