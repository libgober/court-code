# illustrates downloading the case information from justia. Grabs the names and urls of all opinions from a date range specified
# is good at extracting most content, does not know how to grab decision dates which would be useful!
#


#libraries
from bs4 import BeautifulSoup
import requests
import lxml
from unicode_support import *
import csv
import re
import time
import random

years = range(2011,2015)
for year in years:

    #path to all cases on Justia from a year
    path = "https://supreme.justia.com/cases/federal/us/year/" + str(year) + ".html"
    
    #grab an RSS feed from oyez
    r = requests.get(path, allow_redirects=False)
    
    #parse it using Beautiful soup library
    soup = BeautifulSoup(r.text, "html")
    
    table = [["title","date","citation","url","cite_error","date_error"]]
    
    #create a table iterating over all items in the RSS feed
    for itm in soup.find_all('div', class_="result"):
        
        #check for title, if no title next case we don't want it
        if (not bool(itm.find("a",class_="case-name"))):
            continue    
        else:
            title = itm.find("a",class_="case-name").text
            url = "https://supreme.justia.com" + itm.find("a",class_="case-name").get("href")
        
        #check for first occurence of something that looks like a citaion
        result = re.search(r"Citation.*?(?P<citation>(?P<reporter>\d*)\s*U.S.\s*(?P<page>\d*))",str(itm),re.UNICODE)
        
        if result:
            citation = result.group("citation")
            #sanity check on result, record error otherwise
            if url == "https://supreme.justia.com/cases/federal/us/" + result.group("reporter") + "/" + result.group("page") + "/":
                cite_error = "0"
            else:
                cite_error = "URL and citation disagree"                
        else:
            citation = ""
            cite_error = "No citation found"
               
        #check for first occurence of soemthing that looks like date
        result = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{1,2},? (\d{2,4})",str(itm),re.UNICODE)
        if result:
            date_decided = result.group(0)
            if int(result.group(2)) == year:
                date_error = "0"
            else:
                date_error = "Year found doesn't match expected"
        else:
            date_error = "No date listed"
            date_decided = str(year)

    
        table.append([title,date_decided,citation,url,cite_error,date_error])    
    
    #list length
    nrows = len(table)
    
    #define save path
    save_path = "CSVs/" + str(year) + "_table.csv"
    
    with open(save_path,'wb') as f:
        writer = UnicodeWriter(f,delimiter="\t")
        for i in xrange(nrows):
            writer.writerow(table[i])
            
    time.sleep(random.randint(5,15))
