# coding=utf-8
from __future__ import print_function

from bs4 import BeautifulSoup
import requests
import csv
# import nltk
import re
import pandas as pd


# ######################################################################
#  This is for all Richmond, VA public libraries
# ######################################################################
# - like DC libraries all library websites are part of the same system,
#   however, their system isn't powered by Drupal
# - These libraries all use libcal
# ######################################################################

def print_element(elem):
    print('__________________________________________________')
    print(elem.prettify())
    print('__________________________________________________\n')


def print_list(l):
    for i in range(len(l)):
        print(i, '-', l[i])


# first get all the links
# ...slightly modified to work for richmond
def get_links_from_url(url):
    return ['http://rvalibrary.libcal.com']
    #turns out we don't need all this:
    res = requests.get(url)
    html = res.content
    soup = BeautifulSoup(html, 'lxml')

    # first get the right piece of the page and write it to a csv
    elem = soup.findAll(text=re.compile('Locations'))[0]  # get the first locations element

    pt = elem.parent.parent  # warning: will not work for elements without 2 parents (rare)
    list_items = pt.find('ul').findAll('li')

    # get links to the pages to from which will then be grabbed the pages with events links
    links = []
    for link in list_items:
        links.append(url + link.find('a', href=True)['href'])

    event_links = []
    for link in links:
        res = requests.get(link)
        html = res.content
        soup = BeautifulSoup(html, 'lxml')
        elem = soup.findAll(text=re.compile('Events'))[0].parent.parent  # get the first locations element
        print(elem.prettify())
        event_links.append(elem.find('a', href=True)['href'])

    with open('links2.csv', 'wb') as f:
        wr = csv.writer(f)
        wr.writerow(links)

    return links


def get_list(file_name):
    l = []
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
    return l[0]


def get_events(links, p_lib, b_url):
    c = 0
    df = pd.DataFrame()
    regex = re.compile('(([\\\\]r|[\\\\]n)([\\\\]r|[\\\\]n)*)|(([\n|\r])([\n|\r])*)')
    for url in links:
        res = requests.get(url)
        html = res.content
        soup = BeautifulSoup(html, 'lxml')

        # if there's an error it's a problem with their being two of the same id in the html

        rows = soup.select('.s-lc-c-evt')

        title = link = date = description = location = ''
        for row in rows:
            h = row.select('.media-heading')[0]
            link = h.find('a', href=True)['href']
            title = h.text.rstrip()
            table = row.find('dl')
            if table is not None:
                table = table.findAll('dd')
                date = table[0].text.rstrip() + ' ' + table[1].text.rstrip()
                location = p_lib + ' - ' + table[2].text
            # description = row.select('.s-lc-c-evt-des')[0].text
            description = regex.sub(' ', row.select('.s-lc-c-evt-des')[0].text).strip()

            df = df.append({
                'Location': location,
                'Title': title,
                'Link': link,
                'Date': date,
                'Description': description},
                ignore_index=True)

        # if c > 0: break  # TODO: remove
        c += 1
        # print('__________________________________________________')
    print(df)
    # df.to_csv('alaska_state_libs_events.csv', sep='\t', encoding='utf-8')


# then go through and take out the needed data from that piece of the page
parent = 'Richmond, VA'
base_url = 'http://rvalibrary.org/'
# l = get_links_from_url(base_url)
# l = ['http://library.state.ak.libcal.com/']  # for testing
l = ['http://library.state.ak.libcal.com/calendar/continuing_education/?cid=5973&t=m&d=2017-10-01&cal%5B%5D=5973&cal%5B%5D=5971']
# l = get_list('links.csv')  # getting list of links
# print_list(l)
get_events(l, parent, base_url)
