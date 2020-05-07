#!/usr/local/bin/python3

import os
import sys
import requests
import re
import random
from bs4 import BeautifulSoup

# Check for the required environment variables
try:
    goodreadsEmail = os.environ['GOODREADS_EMAIL']
    goodreadsPassword = os.environ['GOODREADS_PASSWORD']
    iftttApiKey = os.environ['IFTTT_API_KEY']
except KeyError as e:
    print('Please set the %s environment variable' % e.args[0])
    sys.exit(1)

# Create a session so that we keep the cookies that we need
s = requests.Session()

# Login to goodreads (we first have to load the sign in page to get the hidden
# 'n' and 'authenticity_token' inputs from the sign in form to successfully sign
# in to the site)
r = s.get('https://www.goodreads.com/user/sign_in')
loginPage = BeautifulSoup(r.text, 'html.parser')
n = loginPage.find('input', { 'name': 'n'}).get('value')
authenticityToken = loginPage.find('input', { 'name': 'authenticity_token'}).get('value')
loginData = {
   'user[email]': goodreadsEmail,
   'user[password]': goodreadsPassword,
   'authenticity_token': authenticityToken,
   'n': n
}
r = s.post('https://www.goodreads.com/user/sign_in', data=loginData)

# Get the user ID from the page that loaded
userFeedUrl = BeautifulSoup(r.text, 'html.parser').find('link', { 'title': 'Goodreads' }).get('href')
userId = re.search('index_rss/(.+?)\?', userFeedUrl).group(1)

# Now that we are logged in, we can get the list of books that have highlights
r = s.get('https://www.goodreads.com/notes/%s/load_more' % userId)
print('Found %i books with highlights' % len(r.json()['annotated_books_collection']))

# Get the info and reading notes URL for each book
books = list(map(lambda x: { 'title': x['title'], 'author': x['authorName'], 'highlightsUrl': x['readingNotesUrl'], 'imageUrl': x['imageUrl'] },
    r.json()['annotated_books_collection']))

# Build a list of all highlights
highlights = []
for book in books:
    print('Fetching highlights for ' + book['title'])
    r = s.get(book['highlightsUrl'])
    highlights.extend(list(map(lambda x: { 'title': book['title'], 'author': book['author'], 'imageUrl': book['imageUrl'], 'highlight': x.find('span').text }, BeautifulSoup(r.text, 'html.parser').findAll('div', {'class': 'noteHighlightContainer'}))))

print('Total highlights found: %i' % len(highlights))

# Send a random highlight in a push notification via IFTTT
randomHighlight = random.choice(highlights)
data = {
    'value1': '%s (%s)' % (randomHighlight['title'], randomHighlight['author']),
    'value2': randomHighlight['highlight'],
    'value3': randomHighlight['imageUrl']
}
requests.post('https://maker.ifttt.com/trigger/daily_highlight/with/key/%s' % iftttApiKey, data=data)
