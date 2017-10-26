# coding=utf-8
from bs4 import BeautifulSoup
import requests
import csv
import nltk
import re

import matplotlib.pyplot as plt
import seaborn as sns

res = requests.get('https://sfpl.org/index.php?pg=2000172901&loc=1')
html = res.content
sp = BeautifulSoup(html, 'lxml')

fl = open("test2.txt", "w")
fl.write(sp.prettify())
fl.close()


# one other thing to do is using scrapely

"""
>>> from scrapely import Scraper
>>> s = Scraper()
>>> train_url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'
>>> s.train(train_url, {'name':'Afghanistan','population':'29,121,286'})
>>> test_url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
>>> s.scrape(test_url)
[{u'name': [u'United Kingdom'], u'population': [u'62,348,447']}]
>>> s.scrape('http://example.webscraping.com/places/default/view/Aland-Islands-2')
[{u'name': [u'Aland Islands'], u'population': [u'26,711']}]
"""