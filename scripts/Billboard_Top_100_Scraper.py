"""
Script to enable scraping of Billboard Hot 100 data from Wikipedia using the 
requests and BeautifulSoup libraries. Data is exported as a csv file.

"""

import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import unicodecsv


res = []
url = 'https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_'
year = 2014

html = requests.get(url+str(year))
soup = BeautifulSoup(html.text, 'lxml')
for entry in soup.find_all('tr'):
    if len(entry.find_all('td')) >= 2: # note change here
        row = {}
        for e in entry.find_all('th'): # also here
            row['date'] = e.text+" "+str(year)
        for i, e in enumerate(entry.find_all('td')):
            if i == 0:
                row['title'] = e.text
                if 'rowspan' in e.attrs:
                    row['weeks'] = int(e['rowspan'])
                else:
                    row['weeks'] = 1
            elif i == 1:
                row['artists'] = e.text
            else:
                continue
        if len(row) == 4:
            res.append(row)

# Clean missing artists and Lady Marmalade cover, add 'entry' variable
title_count = defaultdict(int)
res_updated = []
prev_artist = ""
for e in res:
    row = e
    if ("[" in e['artists'] or e['artists'] == "")    and len(e['artists']) < 5:
        row['artists'] = prev_artist
    title_count[e['title']+e['artists']] += 1
    row['entry'] = title_count[e['title']+e['artists']]
    if e['title'] == '"Lady Marmalade"' and "Christina" in e['artists']:
        row['title'] = '"Lady Marmalade (Moulin Rouge)"'
    prev_artist = e['artists']
    res_updated.append(row)

# Clean year end transitions
res_updated2 = []
for i in range(0,len(res_updated) - 1):
    if "December" in res_updated[i]['date'] and "January" in res_updated[i+1]['date'] \
        and res_updated[i]['title'] == res_updated[i+1]['title']:
        row = res_updated[i]
        row['weeks'] = res_updated[i]['weeks'] + res_updated[i+1]['weeks']
        res_updated2.append(row)
    elif "December" in res_updated[i-1]['date'] and "January" in res_updated[i]['date'] \
        and res_updated[i-1]['title'] == res_updated[i]['title']:
        continue
    else:
        res_updated2.append(res_updated[i])

# Consolidate titles
res_by_title = defaultdict(dict)
for e in res_updated2:
    row = {}
    row['artists'] = e['artists']
    row['title'] = e['title']
    row['entry_{0}'.format(e['entry'])] = e['date']
    row['weeks_{0}'.format(e['entry'])] = e['weeks']
    res_by_title[e['title']+e['artists']].update(row)

# Return to list form
res_final = []
for key,value in res_by_title.items():
    res_final.append(value)

# Prepare fields for csv export.
csv_fields = ['title','artists','entry_1','entry_2',
              'entry_3','weeks_1','weeks_2','weeks_3']

# Export csv
with open('../data/Billboard_Top_100_'+str(year)+'.csv', 'wb') as f:
    writer = unicodecsv.DictWriter(f, csv_fields)
    writer.writeheader()
    writer.writerows(res_final)