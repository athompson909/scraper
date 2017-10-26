# coding=utf-8
from __future__ import print_function

from bs4 import BeautifulSoup
import requests
import csv
import nltk
import re


def print_element(elem):
    print('__________________________________________________')
    print(elem.prettify())
    print('__________________________________________________\n')


def print_list(l):
    for i in range(len(l)):
        print(i, '-', l[i])


# first get all the links
def get_links_from_url():
    url = 'https://www.dclibrary.org'
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
    with open("links.csv", 'wb') as f:
        wr = csv.writer(f)
        wr.writerow(links)

    return links


def get_list(file_name):
    l = []
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
    return l[0]


# then go through and take out the needed data from that piece of the page
# links = get_links_from_url()
links = get_list('links.csv')
# print_list(links)

