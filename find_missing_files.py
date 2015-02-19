#Comes through directory and finds directories containing no files, creates CSV of cases where files are expected
# To use specify as the first command the parent directory
# Then the next commands give start year and end year for competeness search
# The expected directory structure looks like
# Parent
#  | 1800
#  | 1801
#  ...
#  | 2000
#       | - 1 Joe v. Shmo
#       | - 2 Do v. Mo

import glob
import sys
import os
import csv
import re

def main(year, parent_folder_path):
    with open(parent_folder_path + "Missing/" + str(year) + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
    
        #Folder of a year containing cases
        year_folder_path = parent_folder_path + str(year) + "/"
        
        #Open each folder in the year folder path
        for folder in os.listdir(year_folder_path):
            if not folder[0].isdigit():
                print("Skipping" + folder + "not a case folder")
                continue
            else:
                if not os.listdir(year_folder_path + folder):
                    print(folder + "is empty")
                    
                    #First break the path into its meta data, assuming form ### CASE NAME, ### U.S. ###
                    search = re.search("(\d{1,3})\s(.*),\s(\d{1,3}\s\U\.S\.\s\d{1,4})?",folder)
                    
                    #case number
                    case_number = search.group(1)
            
                    #get the case name as contained in the file_path
                    name = search.group(2)
                    
                    #get the case citation as contained in the file_path
                    citation =search.group(3)
                            
                    #create case_id by append case year to case number (will be zero-filled by SQL to XXXYYYY) 
                    case_id = case_number + str(year)
                    
                    writer.writerow([year,case_number,case_id,name,citation])
                    




parent_folder_path = sys.argv[1]

#Start year
start_year = int(sys.argv[2])

#Note that the end year will not be scanned!
end_year = int(sys.argv[3]) 
for i in xrange(start_year, end_year):
    main(i,parent_folder_path)