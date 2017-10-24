# coding=utf-8
"""
practice project:

- crawl top news web pages and get lists of top events with their summaries
- export data to a csv
"""
from __future__ import print_function

from bs4 import BeautifulSoup
# import requests
# import csv
# import nltk
# import re
#
# import numpy as np
import pandas as pd


def scrape(soup):
    # print(soup)
    stories = soup.findAll(attrs={'class': 'story'})
    print("All stories:\n")
    print("test")
    df = pd.DataFrame()  # columns=['Title', 'Link', 'Author(s)', 'Summary'])
    for story in stories:
        title = author = link = sumhtml = summary = ''

        # print(story)
        heading = story.find('h2')
        # print(heading)
        if heading is not None:
            heading_a = heading.find('a', href=True)
            if heading_a is not None:
                title = heading_a.text
                link = heading_a['href']
            else:
                continue

        byline = story.find('p', attrs={'class': 'byline'})
        if byline is not None:
            author = byline.text

        sumhtml = story.find('p', attrs={'class': 'summary'})
        if sumhtml is not None:
            summary = sumhtml.text

        df = df.append({'Title': title, 'Link': link, 'Author(s)': author, 'Summary': summary}, ignore_index=True)


### GETTING THE DATA: ###
# response = requests.get('https://www.nytimes.com/')
# html = response.content

fl = open("test.txt", "r")  # just getting text from test.txt
sp = BeautifulSoup(fl.read(), 'lxml')
fl.close()

# html = ''
# sp = BeautifulSoup(html, 'lxml')
scrape(sp)
