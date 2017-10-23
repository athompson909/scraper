from bs4 import BeautifulSoup
import requests
import csv
import nltk
import re

import matplotlib.pyplot as plt
import seaborn as sns

from lxml.html import fromstring

# url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
# url = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
# res = requests.get(url)
#
# soup = BeautifulSoup(res.content, 'lxml')  # instead of 'html5lib'
# fixed_html = soup.prettify()
#
# print(fixed_html)

url = 'https://en.wikipedia.org/wiki/Kragujevac_massacre'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'lxml')

# table = soup.find('tbody', attrs={'class': 'stripe'})
# print table.prettify()

tokens = re.findall('\w+', soup.text)

sw = nltk.corpus.stopwords.words('english')

words_ns = []
for word in tokens:
    if word not in sw:
        words_ns.append(word)

# %matplotlib inline
# sns.set()

freqdist1 = nltk.FreqDist(words_ns)
freqdist1.plot(25)

# tokenizer = nltk.RegexpTokenizer('\w+')
# tokens = tokenizer.tokenize(text)
print(tokens)


# list_rows = []
# for row in table.findAll('tr'):
#     # print row.prettify()
#     list_cells = []
#     for cell in row.findAll('td'):
#         # print(cell.text.replace('&nbsp;', ''))
#         text = cell.text.encode('utf-8')
#         text = text.replace('&nbsp', '')
#         text = text.replace('\n', '')
#         text = text.replace('\xa0', '')
#         text = text.replace('\xc2', '')
#         list_cells.append(text)
#     print(list_cells)
#     list_rows.append(list_cells)
#
# # print(list_rows)
#
# outfile = open('./test.csv', 'wb')
# writer = csv.writer(outfile)
# writer.writerows(list_rows)


# scraper callback:
def scrape_callback(url, html):
    fields = ('area', 'population', 'iso', 'country', 'capital',
              'continent', 'tld', 'currency_code', 'currency_name',
              'phone', 'postal_code_format', 'postal_code_regex',
              'languages', 'neighbours')
    if re.search('/view/', url):
        tree = fromstring(html)
        all_rows = [
            tree.xpath('//tr[@id="places_%s__row"]/td[@class="w2p_fw"]' % field)[0].text_content()
            for field in fields]
        print(url, all_rows)
