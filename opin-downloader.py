#!/usr/bin/python
#Opinion Downloader
#
#blibgober@g.harvard.edu
#
#With a CSV containing information about all Supreme Court opinions 
#from a given year, open CSV, find URL, download opinion, save the file.  
# The only difference from previous is that now with command line

# This version now carries more robust error and incident control
# It also notifies me via email that an issue has come up and/or been resolved

import csv
import requests
from bs4 import BeautifulSoup
import itertools
import codecs
import os.path
import os
import time
import random
import sys
import smtplib


def wake_master(message):
    sender = 'r3k790@gmail.com'
    receivers = 'blibgober@g.harvard.edu'
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login("r3k790","Aa571423")
    server.sendmail(sender, receivers, message)     
    server.quit()    
    print "Successfully sent email"

def downloader(year,start=1):
    path = "/Users/brianlibgober/Box Sync/Backup/Justia/CSVs/" + str(year) + "_table.csv"
    save_path = "/Users/brianlibgober/Box Sync/Backup/Justia/" + str(year) + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    fail_count = 0
    with open (path, 'rb') as fin:
        table = csv.reader(fin, delimiter="\t")
        for row in itertools.islice(table,start,None):
            url = row[3] + "case.html"
            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                print "Connection was Interrupted... Will Try Again in Two Minutes"
                time.sleep(120)
                fail_count += 1	
                if fail_count == 3:
                    wake_master("""From: Alan Stuart <r3k790@gmail.com>
                    To: Brian <blibgober@g.harvard.edu>
                    Subject: Failure in Downloading Application
                    
                    Dear Master,
                    An issue has come up with the downloading apparatus. HELP!
                    Best,
                    Python
                    """)
                continue
                             
            safe_case_name = str(row[0]).replace("/","-")
            save_file_name = str(start) + " " + safe_case_name  + ", " + row[2] + ".txt"
            with codecs.open (save_path+save_file_name,mode="w+", encoding="utf-8-sig") as fout:
                fout.write(r.text)
            print "Succesfully Wrote " + save_file_name + " "  + time.asctime(time.localtime())
            start += 1
            if fail_count > 3:
                wake_master("""From: Alan Stuart <r3k790@gmail.com>
                To: Brian <blibgober@g.harvard.edu>
                Subject: Succesful Recovery in Downloading Application
                
                Dear Master,
                The issue that came up with the downloading apparatus has been solved.
                Best,
                Python
                """)
            fail_count = 0
            time.sleep(random.randint(5,20))

try:
    start = int(sys.argv[3])
except IndexError: 
    start = None
    
for i in xrange(int(sys.argv[1]),int(sys.argv[2]),-1):
    downloader(i,start)
    wake_master("""From: Alan Stuart <r3k790@gmail.com> \nTo: Brian <blibgober@g.harvard.edu>\nSubject: Year """ + str(i) + 
    """Success!\n Dear Master,\nJust thought you'd like to know.\n Best,\n Python
""")

wake_master("""From: Alan Stuart <r3k790@gmail.com>
To: Brian <blibgober@g.harvard.edu>
Subject: Finished Downloading Files

Dear Master,
I await your instructions 
Best,
Python
""")

#Interrupted download can be triggered with this
#downloader(sys.argv[1],start)