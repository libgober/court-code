# A new version of the old processor, which worked well so I saved it before I fiddled and ruined
#Brian Libgober: blibgober@g.harvard.edu
#In this file we take an input of the raw HTML received from requesting an opinion
#Then we add the word counts to a MySQL database.  
#The main steps are getting the file, creating a hash table of words and their frequency scores, and then uploading that table to the database.
#Before I do the count, however, I need to make sure there isn't junk in the text that will bias the scores.
#The most egregious junk is the disclaimer about reliability. Other junk includes citations and a summary syllabus at the begining, which is harder to eliminate. 
#By segregating the function I allow arbitrarily good processing of junk. 
#Additionally, I upload some meta-data on each file that will allow me to do some joins later


import pyodbc #for MySQL interaction
from bs4 import BeautifulSoup #for parsing our text files
import codecs
from collections import Counter 
import re
import glob
import sys

def add_data(case_id,key,value):

    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')

    #cnxn = pyodbc.connect('Driver={MySQL ODBC 5.3 Unicode Driver};SERVER=127.0.0.1;DATABASE=Court;user=jharvard;password=crimson')
    
    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
    #add the counts to MySQL
    cursor.execute("insert into word_count(case_id,word,frequency) values (?,?,?)",case_id,key,value)

    #commit the connection to save these values
    cnxn.commit()
    
def add_meta_data(case_id,name,year,citation):
    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')
    
    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
     #add meta data to another table in same database
    cursor.execute("insert into bdl_opinion_cat(case_id,name,year_decided,citation) values (?,?,?,?)",case_id,name,year,citation)
    
    #commit the connection to save these values
    cnxn.commit()
    
def evacuate(string):
    disclaimer = "Official Supreme Court case law is only found in the print version of the United States Reports\. Justia case law is provided for general informational purposes only, and may not reflect current legal developments, verdicts or settlements\. We make no warranties or guarantees about the accuracy, completeness, or adequacy of the information contained on this site or information linked to from this site\. Please check official sources\."
    string = re.sub(disclaimer,"",string,count=0)
    string = string.lower()
    return string

def count_words(read_path):
    
    #load HTML
    html = open(read_path, "r")
    
    #Parse HTML into beautiful soup
    soup = BeautifulSoup(html)
    
    #Extract opinion
    opinion_html = soup.find(id="opinion")
    
    #Convert Opinion HTML to String
    opinion = opinion_html.get_text(" ",strip=True)
    
    #Expel materials that are not actually part of opinion (e.g. disclaimers, information about parties, docket no.)
    opinion = evacuate(opinion)
    
    #Divide the text of the opinion into a list of words and then count them
    tabulation = Counter(re.findall(r'\w+',opinion))
    
    return tabulation

def main(year):
    #folder_path of year to churn through
    folder_path = "/Users/brianlibgober/Box Sync/Backup/Justia/" + str(year) + "/"
    
    #iterate over all the opinion files in a given folder
    for file_path in glob.iglob(folder_path + "*.txt"):
        print("Working on" + file_path)
          
        #count the words in the file
        tabulation = count_words(file_path)
        
        #break the path into its meta data, assuming form ### CASE NAME, ### U.S. ### 
        search = re.search("(\d{1,3})\s(.*),\s(\d{1,3}\s\U\.S\.\s\d{1,4})",file_path)
        case_number = search.group(1)
        
        #get the case name as contained in the file_path
        name = search.group(2)
        
        #get the case citation as contained in the file_path
        citation =search.group(3)
        
        #create case_id by append case year to case number (will be zero-filled by SQL to XXXYYYY) 
        case_id = case_number + str(year)
        
        add_meta_data(case_id,name,year,citation)
    
        #upload count to database
        for entry in tabulation.items():
            add_data(case_id,entry[0],entry[1])
        
        print("    Succesfuly Added " + file_path)

#for i in xrange(int(sys.argv[1]),int(sys.argv[2]),-1)

for i in xrange(int(sys.argv[1]), int(sys.argv[2])):
    main(i)