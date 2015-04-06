# This module contains functions that help with handling the logistics of doing frequency count analysis on the supreme court opinoions.  
#Throughout we assume a directory structure like
#  Parent
#   |-1800
#   |-1801
#   ...
#   |-2014
#       | - Opinion Folder
#           |- Opinion File #1
#           |- Opinion File #2 etc.


#
# The goal of this and related functions is to make it so that all file saving and handling is taken care of
# and we can therefore focus on experimenting with different kinds of text analyses.

import argparse
import os
import csv, codecs, cStringIO
from collections import Counter 
import re

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def prompt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help="The parent folder that contains all the opinion years. Defaults to current working directory", default=".")
    parser.add_argument("--save", help="The name of the file to save. Default is results.tsv", type=argparse.FileType('ab+'), default="./results.tsv")
    parser.add_argument("--start", help="The year to start scanning. Default is 1800.", type=int, default=1800)
    parser.add_argument("--end", help="The latest year to scan. It is inclusive, so if the last year to scan is 2014 then put 2014, not 2015.", type=int, default=2014)
    parser.add_argument("--top", help = "The highest row to scan.", default=1,type=int)
    parser.add_argument("--bottom", help="The final row to scan, inclusive. If the last case number is 79 then write 79, not 80.",type=int)
    args = parser.parse_args()
    
    if not (args.root[-1] == "/"):
        args.root = args.root + "/"
    
    return([args.save,args.root,args.start,args.end,args.top,args.bottom])


#Input is a list of list of pairs, output must be a list of tuples
def default_flattener(list_of_list):
    final = {}
    for list_of_pairs in list_of_list:
        final.update(list_of_pairs)
    print(final)
    return(final)
    


#queuer handles the application of the analyzer function to a set of documents. 
def queuer(analyzer,headers=[],flattener=default_flattener,skip_list=[],save="./results.tsv",root=".",start=1800,end=2015,top=1,bottom=None):
    if flattener == None:
        flattener = default_flattener
    
    #open the save file for writing
    with save:
        writer = UnicodeWriter(save, delimiter = "\t")
        #check if the file previously existed
        if os.stat(save.name).st_size == 0:
            writer.writerow(headers)
        
        #Now we assume we're at the end of the file since save is in append mode    
        
        #Iterate over the requested list of years
        for year in xrange(start,end+1):
            print("Starting work on " + str(year))
            year_folder_path = root + str(year) + "/"
            
            #Iterate over the opinions in a year folder
            for folder in os.listdir(year_folder_path):
                
                #We don't want to iterate over hidden directories which start with dot or other weird characters
                if folder[0] in [".","*"]:
                    continue
                    
                #break apart the name into its metadata, assuming form ### CASE NAME, ### U.S. ### 
                search = re.search("(\d{1,3})\s(.*),\s(\d{1,3}\s\U\.S\.\s\d{1,4})?",folder)
                
                #case number
                case_number = search.group(1)
                
                #get the case name as contained in the file_path
                name = search.group(2)
                
                #get the case citation as contained in the file_path
                citation =search.group(3)
               
                #don't want to allow no values for bottom so we'll set it to a safe large value
                if bottom == None:
                    bottom = 1000 
                                                                        
                #if the case number is not in the list to search, skip
                if not (int(case_number) in range(top,bottom+1)):
                    continue
                
    ###########
    ###########  At this point we have loaded case name, case number, citation into memory.
    ###########
    
                #Now we have to see what files are inside a case folder and then analyze them, returning something that looks like a table
                
                #get case_folder name
                case_folder = year_folder_path + folder
                if not (case_folder[-1] == "/"):
                    case_folder = case_folder + "/"
                
                #list files inside
                opinion_files = os.listdir(case_folder)
                
                #remove elements that are on our skip list by using set substraction
                opinion_files = list(set(os.listdir(case_folder)) - set(skip_list))
                
                if len(opinion_files) == 0:
                    print("I didn't find any files to add in " + case_folder + "so I'm moving on.")
                    continue
        
                elif len(opinion_files) == 1:
                    document_path = case_folder + opinion_files[0]
                    output = analyzer(open(document_path,"r"))
                
                #because there are several documents in the folder we will have to apply a flattener function,
                #which is a rule about how to combine the application of analyzer to several items in a folder
                
                else:
                    preoutput = []
                    for filepath in opinion_files:
                        #skip hidden files
                        if filepath[0] == ".":
                            continue
                        else:
                            document_path = case_folder + filepath
                            preoutput.append(analyzer(open(document_path,"r")))
                    
                    output = flattener(preoutput)
                
            
    ############# Now we have some output for each case, we want to save it by writing to the tsv
    ############## I assume it's a counter type object
    
                #create case_id to attach to 
                case_id = case_number + str(year)
            
                for row in output.items():
                    if citation is None:
                        citation = u"None"
                    what_to_print = row + (citation,case_number,unicode(year))
                    print(what_to_print)
                    writer.writerow(what_to_print)



############### OTHER USEFUL FUNCTIONS


#Cleans up certain issues I was noticing in how bs4 produces strings
def string_fixes(souptext):
    return(souptext)


