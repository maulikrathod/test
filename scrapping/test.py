import urllib2

url = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"

page = urllib2.urlopen(url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(page, "lxml")
# print "#"*50,soup

####################### also use requests modules
# import requests
#
# page1 = requests.get("https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India")
# print page1
#
# soup1 = BeautifulSoup(page1.content, "html.parser")
# print "*"*50,soup1
#############################################################

# print soup.prettify()
# print soup.title.string

"""find all link from a tag"""
# all_links = soup.find_all('a')
# for link in all_links:
#     print link.get("href")

"""find table"""
all_tables = soup.find_all("table")
right_table = soup.find("table", class_="wikitable sortable plainrowheaders")
# print right_table
# Generate Lists
a, b, c, d, e, f, g = [], [], [], [], [], [], []
for row in right_table.findAll("tr"):
    cells = row.findAll("td")
    states = row.findAll("th")
    if len(cells) == 6:
        a.append(cells[0].find(text=True))
        b.append(states[0].find(text=True))
        c.append(cells[1].find(text=True))
        d.append(cells[2].find(text=True))
        e.append(cells[3].find(text=True))
        f.append(cells[4].find(text=True))
        g.append(cells[5].find(text=True))

# rows = zip(a,b,c,d,e,f,g)
# import pdb;pdb.set_trace()
# print type(c)
# import csv
# from itertools import izip
#
# csvFile = open('csvExample.csv', "wb")
# with csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerow(izip(a,b,c,d,e,f,g))
#
#     for row in rows:
#         writer.writerow(row)

import pandas as pd

df = pd.DataFrame(a, columns=['Number'])
df['State/UT'] = b
df['Admin_capitals'] = c
df['Legislative_Capital'] = d
df['Judiciary_Capital'] = e
df['Year_Capital'] = f
df['Former_Capital'] = g

df.to_csv('csvExample.csv', sep='\t', encoding='utf-8')

# print df
