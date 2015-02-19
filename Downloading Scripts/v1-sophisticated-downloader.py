# This does a better job than the last downloader at grabbing content that is not so predictably named. 
#It uses CSS selectors to interact with the website in a way more similar to a human

import requests
from bs4 import BeautifulSoup #for parsing our text files
from bs4 import SoupStrainer
import itertools
import csv
import codecs
import os.path
import os
import time
import sys


def csvloader(year,number):
    path = "/Users/brianlibgober/Box Sync/Backup/Justia/CSVs/" + str(year) + "_table.csv"
    table = []
    with open (path, 'rb') as fin:
        reader = csv.reader(fin, delimiter="\t")
        for row in itertools.islice(reader,number,None):
            table.append(row)
        return table

def extractor(toc,url):
    #define an empty array for storing the texts we download
    texts = []
    names = []
    bullets = toc.find_all('li')
    #bullets.pop(0)
    #grab an anchor containing a link we want
    for li in bullets:
        #define the anchor, assuming it exists
        anchor = li.a
        #grab the link extension contained in the anchor, if it exists
        if anchor is not None:
            link_extension = anchor.get('href')
        else:
            link_extension = ""
        #use the extension to get text at the url we want to lookup
        text = requests.get(url+link_extension).text
        #add text to our collection
        texts.append(text)
        
        #get the displayed text out of the link
        displayed = [text for text in li.stripped_strings]
        names.append(' '.join(displayed))
    
    return [texts,names]

#to save the file
def saver(year,number,raw_pages,names,meta_data):
    #we create a folder for every year, then a folder for every opinion, and then the texts all in separate files
    save_parent_folder = "/Users/brianlibgober/Box Sync/Backup/Justia/" + str(year) + "/"
    if not os.path.exists(save_parent_folder):
        os.makedirs(save_parent_folder)
    safe_case_name = str(meta_data[0]).replace("/","-")
    save_folder = save_parent_folder + str(number) + " " + safe_case_name + ", " + meta_data[2] + "/"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    for i in range(len(names)):
        save_file_name = save_folder + names[i].encode('utf-8') + ".txt"
        with codecs.open (save_file_name,mode="w+", encoding="utf-8-sig") as fout:
            fout.write(raw_pages[i])

def main(year,start):
    #load csv as array
    table = csvloader(year,start)
    
    for i in range(len(table)):
        number = i + start
    
        #take row's metadata
        meta_data = table[i]
        
        #get the url
        url = meta_data[3]
        #load page,soupify, and store for usage.
        index = requests.get(url).text
        #Create special parsers for faster loading that we will use throughout
        toc_parser= SoupStrainer(class_="centered-list clear")
            
        #find the centered list which serves as the table of contents
        toc = BeautifulSoup(index,"html.parser",parse_only=toc_parser)
        
        #extract the links and request the pages to get a list of the subelements and names we can use for saving
        raw_content = extractor(toc,url)
        #split this into two, the names and the opinion text
        raw_pages = raw_content[0]
        #names associated with the opinions
        raw_names = raw_content[1]
        #save content at links -  This will allow for the maximum flexibility in dealing with content later
        saver(year,number,raw_pages,raw_names,meta_data)
        print("Downloaded and Saved " + str(number) + " " + meta_data[0])

#Queue manager
#supply year and number
#start = int(sys.argv[3])
#for i in xrange(int(sys.argv[1]),int(sys.argv[2]),-1):
 #   main(i,start)
 
for year in xrange(2013,2014):
    main(year,1)