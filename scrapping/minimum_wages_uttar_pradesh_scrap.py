import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.labourlawreporter.com/2017/minimum-wages-uttar-pradesh/"

page = requests.get(url)
if page.status_code == 200:
    print "SUCCESS",page.status_code
else:
    print "else:", page.status_code

soup = BeautifulSoup(page.content, "html.parser")

# find required table
right_table = soup.find("table", width="1245")
a,b,c,d,e,f,g,h,i,j,k = [],[],[],[],[],[],[],[],[],[],[]
for row in right_table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 11:
        a.append(cells[0].find(text=True))
        b.append(cells[1].find(text=True))
        c.append(cells[2].find(text=True))
        d.append(cells[3].find(text=True))
        e.append(cells[4].find(text=True))
        f.append(cells[5].find(text=True))
        g.append(cells[6].find(text=True))
        h.append(cells[7].find(text=True))
        i.append(cells[8].find(text=True))
        j.append(cells[9].find(text=True))
        k.append(cells[10].find(text=True))

df = pd.DataFrame(a, columns=["Sr.No."])
df['industry name'] = b
df['Un-Skilled Basic Minimum Wage'] = c
df['Un-Skilled V.D.A'] = d
df['Un-Skilled total Wages'] = e
df['Semi-Skilled Basic Minimum Wage'] = f
df['Semi-Skilled V.D.A'] = g
df['Semi-Skilled total Wages'] = h
df['Skilled Basic Minimum Wage'] = i
df['Skilled V.D.A'] = j
df['Skilled total Wages'] = k


# print df
df.to_csv('minimum_wages_uttar_pradesh_scrap.csv', mode='w', encoding='utf-8')
