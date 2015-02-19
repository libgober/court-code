#!/usr/bin/python
#Opinion Downloader
#
#blibgober@g.harvard.edu
#
#With a CSV containing information about all Supreme Court opinions 
#from a given year, open CSV, find URL, download opinion, save the file.  

import csv
import requests
from bs4 import BeautifulSoup
import itertools
import codecs
import os.path
import os
import time
import random

def downloader(year,start=1):
    path = "/Users/brianlibgober/Box Sync/Backup/Justia/CSVs/" + str(year) + "_table.csv"
    save_path = "/Users/brianlibgober/Box Sync/Backup/Justia/" + str(year) + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    with open (path, 'rb') as fin:
        table = csv.reader(fin, delimiter="\t")
        for row in itertools.islice(table,start,None):
            url = row[3] + "case.html"
            r = requests.get(url)
            safe_case_name = str(row[0]).replace("/","-")
            save_file_name = str(start) + " " + safe_case_name  + ", " + row[2] + ".txt"
            with codecs.open (save_path+save_file_name,mode="w+", encoding="utf-8-sig") as fout:
                fout.write(r.text)
            start += 1
            time.sleep(random.randint(5,25))

for i in xrange(1980,1969,-1):
    downloader(i)

#Interrupted download can be triggered with this
#downloader(1981,57)