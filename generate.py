#!/usr/bin/env python

from collections import defaultdict
import codecs
import json
import os
import pystache
import requests
import time
import netrc
from pygithub3 import Github

repos_in = 'repos.json'
index_in = 'index.mustache'
index_out = 'index.html'

auth = netrc.netrc()
try:
  (login, _, password) = auth.authenticators('api.github.com')
  ghclient = Github(login=login, password=password)
  logged_in = True
except:
  ghclient = Github()
  logged_in = False

def gh_repo(name):
  print('Fetching "%s" repo information...' % name)
  # Use the following for development so you do not hammer the GitHub API.
  #return {'name': name, 'html_url': 'http://google.com', 'homepage': 'http://example.com', 'description': 'Description!'}

  if not logged_in:
    time.sleep(2.0) # Take a nap so GitHub doesn't aggressively throttle us.

  repo = ghclient.repos.get(user='square', repo=name)
  return dict(
    name=repo.name,
    homepage=repo.homepage,
    html_url=repo.html_url,
    description=repo.description
  )

with codecs.open(index_in, 'r', 'utf-8') as f:
  template = pystache.parse(f.read())
with codecs.open(repos_in, 'r', 'utf-8') as f:
  repo_config = json.loads(f.read())

repos = repo_config['repos']
custom = repo_config['custom']

# Multimap of categories to their repos.
categories = defaultdict(list)

# Loop through declared repos, looking up their info on GitHub and adding to the specified categories.
for repo in repos.keys():
  repo_cats = repos[repo]
  repo_data = gh_repo(repo)
  if repo_cats is None:
    repo_cats = ['Other']
  for repo_cat in repo_cats:
    categories[repo_cat].append(repo_data)

# Loop though custom repos adding their data (faked to look like GitHub's) to the specified categories.
for repo_data in custom:
  repo_cats = repo_data['categories']
  if repo_cats is None:
    repo_cats = ['Other']
  for repo_cat in repo_cats:
    categories[repo_cat].append(repo_data)


# Template context that will be used for rendering.
context = {
  'categories': []
}

# Loop over the category names sorted alphabetically (case-insensitive) with 'Other' last.
for category_name in sorted(categories.keys(), key=lambda s: s.lower() if s is not 'Other' else 'z'*10):
  data = {
    'name': category_name,
    'index': category_name.lower(),
    'has_repos_with_images': False,
    'has_repos_without_images': False,
    'repos_with_images': [],
    'repos_without_images': [],
  }

  # Loop over category repos sorted alphabetically (case-insensitive).
  for repo_data in sorted(categories[category_name], key=lambda s: s['name'].lower()):
    name = repo_data['name']
    repo = {
      'name': name,
      'href': repo_data['html_url'],
      'website': repo_data.get('homepage', None),
      'description': repo_data.get('description', None)
    }
    if os.path.exists(os.path.join('repo_images', '%s.jpg' % name)):
      data['repos_with_images'].append(repo)
      data['has_repos_with_images'] = True
    else:
      data['repos_without_images'].append(repo)
      data['has_repos_without_images'] = True

  context['categories'].append(data)

# Render the page HTML using MOOOUUSSTTAACCCCHHEEEEE!
renderer = pystache.Renderer()
html = renderer.render(template, context)

with codecs.open(index_out, 'w', 'utf-8') as f:
  f.write(html)

# Rejoice. If you got this far, it worked!
