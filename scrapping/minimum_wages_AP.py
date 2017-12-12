#!/usr/bin/python
"""minimum-wages-andhra-pradesh"""

"""# import required modules"""
from bs4 import BeautifulSoup
import requests
import urllib2
import pandas as pd
import csv
import os

"""# define url"""
url = "http://www.labourlawreporter.com/2017/minimum-wages-andhra-pradesh/"
page = requests.get(url)

"""# check if page is opened or not"""
if page.status_code == 200:
    print "URL OPEN SUCCESSFULLY",page.status_code
else:
    print "404 Not Found", page.status_code

soup = BeautifulSoup(page.content, "html.parser")

#######################OTHER METHOD#######################################################
# url = "http://www.labourlawreporter.com/2017/minimum-wages-uttar-pradesh/"
#
# page = urllib2.urlopen(url)
# soup = BeautifulSoup(page, "html.parser")
##############################################################################

current_path = os.path.dirname(os.path.abspath(__file__))
dir_name = "csv"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# import pdb;pdb.set_trace()
"""# define csv file name & write headers"""
csvFileName = "minimum-wages_Output_AP.csv"
csvFilePath = os.path.join(current_path, dir_name, csvFileName)
csvFile = open(csvFilePath, "a")
writer = csv.writer(csvFile)
headers = ["Skill","Industry Name","Basic Wages","V.D.A","Total"]
writer.writerow(headers)


"""# find required table"""
right_table = soup.find("table", width="528")

"""# find tr data fromn table"""
for row in right_table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 6:
        final_list = []
        """# only get required data"""
        data_list = [x.find(text=True) for x in cells]
        final_list.extend([data_list[1], "", data_list[2]])
        final_list.extend(data_list[4:])
        print final_list
        writer.writerows([final_list])
        # final_string_list = [x.encode("utf-8") for x in final_list]
        # writer.writerows([final_string_list])
print("File Write SUCCESSFULLY")
csvFile.close()
