# coding=utf-8
"""
practice project:

- crawl top news web pages and get lists of top events with their summaries
- export data to a csv
"""
from __future__ import print_function

from bs4 import BeautifulSoup
import requests
# import csv
# import nltk
# import re
#
# import numpy as np
import pandas as pd


def scrape(soup):
    stories = soup.findAll(attrs={'class': 'story'})

    df = pd.DataFrame()  # columns=['Title', 'Link', 'Author(s)', 'Summary'])
    for story in stories:
        if story is None:
            continue
        title = author = link = summary = ''

        heading = story.find('h2')
        if heading is not None:
            heading_a = heading.find('a', href=True)
            if heading_a is not None:
                title = heading_a.text.strip()
                link = heading_a['href']
            else:
                continue

        byline = story.find('p', attrs={'class': 'byline'}, recursive=False)
        if byline is not None:
            author = byline.text.strip()

        summaries = story.select('.summary')
        # print(story.prettify())
        # print()
        if summaries is not None:
            # if len(summaries) == 0 or summaries[0] == '':
            #     print(story.prettify())
            #     print()
            for row in summaries:
                if row.text != '':
                    summary += row.text.strip()
        else:
            print("*** no summary ***\n")

        # print({'Title': title, 'Link': link, 'Author(s)': author, 'Summary': summary})
        if title != '':
            df = df.append({'Title': title, 'Link': link, 'Author(s)': author, 'Summary': summary}, ignore_index=True)

    print(df)
    df.to_csv('news_articles.csv', sep='\t', encoding='utf-8')


# ### GETTING THE DATA: ###
# #from online:
response = requests.get('https://www.nytimes.com/')
html = response.content
sp = BeautifulSoup(html, 'lxml')

# #from file:
# fl = open("test.txt", "r")  # just getting text from test.txt
# sp = BeautifulSoup(fl.read(), 'lxml')
# fl.close()

# #from text in here
# html = ''
# sp = BeautifulSoup(html, 'lxml')

# then scrape it
scrape(sp)
