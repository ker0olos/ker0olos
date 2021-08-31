#!/usr/bin/python

import os
import sys
import urllib
import subprocess

import praw

from PIL import Image, ImageFilter

_min_votes=50
_min_width = 1920
_min_height = 1080

# default subreddit
_subreddit = 'Animewallpaper'

# search query
_query = ''

reddit = praw.Reddit(
    user_agent="wall.py",
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD']
)

# check if a subreddit and/or a search query are specified
try:
  _subreddit = sys.argv[1]
  _query     = sys.argv[2]
except:
  pass

# where to store cached images
_cache_directory = os.path.expanduser('~/Pictures/.wall/')

subreddit = reddit.subreddit(_subreddit)

# exits if the subreddit doesn't exist

try:
  reddit.subreddit(_subreddit).id
except:
  print('r/{} is not a valid subreddit'.format(subreddit))
  sys.exit(1)

# print welcome message

print('\n--------------------------------------------')
print(('r/{} ~ {}' if _query else 'r/{}').format(_subreddit, _query))
print('--------------------------------------------\n')

def resolveURL(post):
  try:
    urls = []
    for id in post.media_metadata:
      urls.append(dict(id=id, url=post.media_metadata[id]['s']['u']))
    return urls
  except:
    if post.url.lower().startswith('https://i.redd.it/') or post.url.lower().startswith('https://i.imgur.com/'):
      return [ dict(id=post.id, url=post.url) ]
    else:
      return []

def processImage(url, filename):
  urllib.request.urlretrieve(url, filename)

  with Image.open(filename) as img:
    # image is in protrait
    if img.size[0] < img.size[1]:
      resizeImage(img, filename)
      subprocess.Popen(['wall.sh', '-u', filename + '_landscape', '-p', filename ])
    # image is in landscape
    else:
      subprocess.Popen(['wall.sh', '-u', filename ])

def resizeImage(img, filename):
  ratio = _min_height / img.size[1]

  copy_size=(int(img.size[0] * ratio), int(img.size[1] * ratio))
  copy_postion=(int((_min_width * 0.5) - (copy_size[0] * 0.5)), 0)

  # resize the image to fit the desired size with while keeping its aspect ratio
  copy = img.resize(size=copy_size, resample=Image.ANTIALIAS)
  
  # resize the image to stretch to the desired size
  background_copy = img.resize(size=(_min_width, _min_height), resample=Image.ANTIALIAS)

  # blur the background copy of the image
  background_copy = background_copy.filter(ImageFilter.GaussianBlur(radius=25))

  # center the rotated image inside the background
  # background_copy.alpha_composite(copy, dest=copy_postion)
  background_copy.paste(copy, box=copy_postion)
  
  # save the new one image
  background_copy.save(fp=filename + '_landscape', format='jpeg')

for post in subreddit.search(query=_query,sort='hot',time_filter='week') if _query else subreddit.hot(limit=20):
  print(post.title) # print('{}: https://reddit.com{}'.format(post.title, post.permalink))

  # skip posts with unconvincing number of up votes

  if post.score < _min_votes:
    print('  - {} is not enough up votes.'.format(post.score))
    continue

  # resolve all the urls in the post
  # returns a list of ids and urls

  data = resolveURL(post)

  for d in data:
    [ id, url ] = d.values()

    # skip used images

    # if os.path.isfile(os.path.join(_cache_directory, id)):
    #   print('  - already used before')
    #   continue

    # update current wallpaper with the new one

    processImage(url, os.path.join(_cache_directory, id))

    # exit the up after finding one wallpaper that can be used

    sys.exit()
