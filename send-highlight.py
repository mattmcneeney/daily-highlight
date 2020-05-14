#!/usr/local/bin/python3

import os
import sys
import requests
import random
from bs4 import BeautifulSoup

def getAllBooksWithHighlights(goodreadsUserId):
    r = requests.get('https://www.goodreads.com/notes/%s/load_more' % goodreadsUserId)
    return list(map(lambda x: { 'title': x['title'], 'author': x['authorName'], 'highlightsUrl': x['readingNotesUrl'], 'imageUrl': x['imageUrl'] },
    r.json()['annotated_books_collection']))

def getHighlightsFromBook(book):
    print('Fetching highlights for ' + book['title'])
    r = requests.get(book['highlightsUrl'])
    return list(map(lambda x: { 'title': book['title'], 'author': book['author'], 'imageUrl': book['imageUrl'], 'highlight': x.find('span').text }, BeautifulSoup(r.text, 'html.parser').findAll('div', {'class': 'noteHighlightContainer'})))

def sendHighlight(highlight, iftttApiKey):
    print('Sending push notification for highlight from %s' % highlight['title'])
    data = {
        'value1': '%s (%s)' % (highlight['title'], highlight['author']),
        'value2': highlight['highlight'],
        'value3': highlight['imageUrl']
    }
    requests.post('https://maker.ifttt.com/trigger/daily_highlight/with/key/%s' % iftttApiKey, data=data)

def main():
   # Check for the required environment variables
   try:
       goodreadsUserId = os.environ['GOODREADS_USER_ID']
       iftttApiKey = os.environ['IFTTT_API_KEY']
   except KeyError as e:
       print('Please set the %s environment variable' % e.args[0])
       sys.exit(1)

   # Get all books with highlights
   books = getAllBooksWithHighlights(goodreadsUserId)
   print('Total books found: %i' % len(books))

   # Get the highlights for each book
   highlights = sum(list(map(lambda x: getHighlightsFromBook(x), books)), [])
   print('Total highlights found: %i' % len(highlights))

   # Send a random highlight in a push notification via IFTTT
   sendHighlight(random.choice(highlights), iftttApiKey)

if __name__ == '__main__':
   main()
