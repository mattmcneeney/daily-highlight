#!/usr/local/bin/python3

import os
import sys
import requests
import re
import random
from bs4 import BeautifulSoup

# Check for the required environment variables
try:
    goodreadsUserId = os.environ['GOODREADS_USER_ID']
    iftttApiKey = os.environ['IFTTT_API_KEY']
except KeyError as e:
    print('Please set the %s environment variable' % e.args[0])
    sys.exit(1)

# Get the list of books that have highlights
r = requests.get('https://www.goodreads.com/notes/%s/load_more' % goodreadsUserId)
print('Found %i books with highlights' % len(r.json()['annotated_books_collection']))

# Get the info and reading notes URL for each book
books = list(map(lambda x: { 'title': x['title'], 'author': x['authorName'], 'highlightsUrl': x['readingNotesUrl'], 'imageUrl': x['imageUrl'] },
    r.json()['annotated_books_collection']))

# Build a list of all highlights
highlights = []
for book in books:
    print('Fetching highlights for ' + book['title'])
    r = requests.get(book['highlightsUrl'])
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
