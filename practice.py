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

fl = open("test.html", "w")
fl.write(sp.prettify())
fl.close()