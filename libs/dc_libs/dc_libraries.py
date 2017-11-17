# coding=utf-8
from __future__ import print_function

from bs4 import BeautifulSoup
import requests
import csv
# import nltk
import re
import pandas as pd


# ######################################################################
#  This is for all Washington DC public libraries, (managed by Drupal)
# ######################################################################
# - all DC libraries are managed by the same Drupal system, making it
#   easy to get the data from all the websites of DC at once
# - I wonder if there will be other Drupal websites like this and if
#   this file could be a template for them
# ######################################################################

def print_element(elem):
    print('__________________________________________________')
    print(elem.prettify())
    print('__________________________________________________\n')


def print_list(l):
    for i in range(len(l)):
        print(i, '-', l[i])


# first get all the links
def get_links_from_url(url):
    res = requests.get(url)
    html = res.content
    soup = BeautifulSoup(html, 'lxml')

    # first get the right piece of the page and write it to a csv
    elem = soup.findAll(text=re.compile('Locations'))[0]  # get the first locations element

    pt = elem.parent.parent  # warning: will not work for elements without 2 parents (rare)
    # print_element(pt)

    links = []
    for link in pt.select('.leaf'):
        links.append(url + link.find('a', href=True)['href'])

    # print_list(links)
    with open('links.csv', 'wb') as f:
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
    for url in links:
        res = requests.get(url)
        html = res.content
        soup = BeautifulSoup(html, 'lxml')

        library = p_lib + ' - ' + soup.select('#page-title')[0].text  # I can do this cuz it's an id
        # if there's an error it's a problem with their being two of the same id in the html

        events = soup.select('#eventsTab')
        if len(events) > 0:
            rows = events[0].select('.row')
            title = link = date = description = ''
            for row in rows:
                h = row.select('.field-name-title')[0]

                link = b_url + h.find('a', href=True)['href']
                title = h.text
                dts = row.select('.date-display-single')
                if len(dts) > 0:
                    date = dts[0].text
                description = row.select('.field-name-body')[0].text
                df = df.append({
                    'Location': library,
                    'Title': title,
                    'Link': link,
                    'Date': date,
                    'Description': description},
                    ignore_index=True)

        # if c > 0: break  # TODO: remove
        c += 1
        # print('__________________________________________________')
    print(df)
    df.to_csv('dc_libs_events.csv', sep='\t', encoding='utf-8')


# then go through and take out the needed data from that piece of the page
# links = get_links_from_url()
parent = 'Washington DC'
base_url = 'https://www.dclibrary.org'
l = get_list('links.csv')  # getting list of links
# print_list(l)
get_events(l, parent, base_url)
