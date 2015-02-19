#This downloads the cases that were identified as missing
#It opens a tsv in the Missing folder of the parent directory
#Each line of the tsv is a missing file, all we need from this is the year and the row number
#We use the year and row number to look up the URL in our URL directory

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

def saver(year,number,raw_page,meta_data):
    #we create a folder for every year, then a folder for every opinion, and then the texts all in separate files
    save_parent_folder = "/Users/brianlibgober/Box Sync/Backup/Justia/" + str(year) + "/"
    
    if not os.path.exists(save_parent_folder):
        os.makedirs(save_parent_folder)
        
    safe_case_name = str(meta_data[0]).replace("/","-")
    save_folder = save_parent_folder + str(number) + " " + safe_case_name + ", " + meta_data[2] + "/"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)        
    
    save_file_name = save_folder + "Per Curiam Opinion.txt"
    with codecs.open (save_file_name,mode="w+", encoding="utf-8-sig") as fout:
        fout.write(raw_page)

def csvloader(year,number):
    path = "/Users/brianlibgober/Box Sync/Backup/Justia/CSVs/" + str(year) + "_table.csv"
    table = []
    with open (path, 'rb') as fin:
        reader = csv.reader(fin, delimiter="\t")
        for row in itertools.islice(reader,number,number+1):
            table.append(row)
        return table

for f in os.listdir("/Users/brianlibgober/Box Sync/Backup/Justia/Missing/"):
    #ignore hidden files
    if f[0] == ".":
        continue
    else:
        with open("/Users/brianlibgober/Box Sync/Backup/Justia/Missing/" + f, 'rb') as source:
            sourcereader = csv.reader(source, delimiter = "\t")
            for row in sourcereader:
                #extract the info we need for lookup
                year = int(row[0])
                row_number = int(row[1])
                
                #Load the information from the directory corresponding to the missing file
                directory_row = csvloader(year,row_number)
                
                #csvloader returns a table, but actually we just have one element in this case so we flatten it
                directory_row = directory_row[0]
                
                #get the url
                url = directory_row[3]
                
                #download the file; these are all single pages
                raw_page = requests.get(url).text
                
                #save the file
                saver(year,row_number,raw_page,directory_row)

                print(directory_row[3])