#!/usr/bin/env python

from collections import defaultdict
import codecs
import json
import os
import pystache
import requests

repos_in = 'repos.json'
index_in = 'index.mustache'
index_out = 'index.html'

def gh_repo(name):
  print('Fetching "%s" repo information...' % name)
  r = requests.get('https://api.github.com/repos/square/%s' % name)
  if r.status_code is not 200:
    raise Exception('GitHub API call for repo "%s" failed with %s.' % (name, r.status_code))
  return json.loads(r.text)

with codecs.open(index_in, 'r', 'utf-8') as f:
  template = pystache.parse(f.read())
with codecs.open(repos_in, 'r', 'utf-8') as f:
  repos = json.loads(f.read())

repo_data = {}
for repo in repos.keys():
  # Use the following for development so you do not hammer the GitHub API
  #repo_data[repo] = {'name': repo, 'html_url': 'http://google.com', 'homepage': 'http://example.com'}
  repo_data[repo] = gh_repo(repo)

categories = defaultdict(list)
for repo in sorted(repos.keys(), key=lambda s: s.lower()):
  repo_cats = repos[repo]
  if repo_cats is None:
    repo_cats = ['Other']
  for repo_cat in repo_cats:
    categories[repo_cat].append(repo_data[repo])

# Assemble template context.
context = {
  'categories': []
}
for category in sorted(categories.keys(), key=lambda s: s.lower() if s is not 'Other' else 'z'*10):
  data = {
    'name': category,
    'index': category.lower(),
    'has_repos_with_images': False,
    'has_repos_without_images': False,
    'repos_with_images': [],
    'repos_without_images': [],
  }
  for repo_data in categories[category]:
    name = repo_data['name']
    repo = {
      'name': name
    }
    if 'html_url' in repo_data:
      repo['href'] = repo_data['html_url']
    if 'homepage' in repo_data:
      repo['website'] = repo_data['homepage']
    if os.path.exists(os.path.join('images', '%s.jpg' % name)):
      data['repos_with_images'].append(repo)
      data['has_repos_with_images'] = True
    else:
      data['repos_without_images'].append(repo)
      data['has_repos_without_images'] = True

  context['categories'].append(data)

# Render the page HTML.
renderer = pystache.Renderer()
html = renderer.render(template, context)

with codecs.open(index_out, 'w', 'utf-8') as f:
  f.write(html)

# Rejoice. If you got this far, it worked!
