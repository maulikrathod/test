##!/usr/bin/python
## minimum-wages-uttar-pradesh"""

## import required modules
from bs4 import BeautifulSoup
import requests
import urllib2
import csv, os

## define url
url = "http://www.labourlawreporter.com/2017/minimum-wages-uttar-pradesh/"
page = requests.get(url)

## check if page is opened or not
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

## It will create 'csv' dir and save all csv files into it
current_path = os.path.dirname(os.path.abspath(__file__))
dir_name = "csv"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

## define csv file name & write headers
csvFileName = "minimum-wages_Output_UP.csv"
csvFilePath = os.path.join(current_path, dir_name, csvFileName)
csvFile = open(csvFilePath, "a")
writer = csv.writer(csvFile)
writer.writerow(["Skill","Industry Name","Basic Wages","V.D.A","Total"])


## find required table
right_table = soup.find("table", width="1245")
## define tuple of skill set
skill_list = ("Un-Skilled",	"Semi-Skilled",	"Skilled")
## find tr data fromn table
for row in right_table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 11:
        ## only get required data
        data_list = [x.find(text=True) for x in cells]
        unskilled_list = data_list[2:5]
        semi_skilled_list = data_list[5:8]
        skilled_list = data_list[8:]
        for skill in skill_list:
            final_list = []
            final_list.extend([skill,data_list[1]])
            if skill == "Un-Skilled":
                final_list.extend(unskilled_list)
            elif skill == "Semi-Skilled":
                final_list.extend(semi_skilled_list)
            elif skill == "Skilled":
                final_list.extend(skilled_list)

            final_string_list = [x.encode("utf-8") for x in final_list]
            ## write final_list data into csv file
            writer.writerows([final_string_list])

print("File Write SUCCESSFULLY")
csvFile.close()
