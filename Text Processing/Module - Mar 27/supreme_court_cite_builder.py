# -*- coding: utf-8 -*-
#To create a script, you need to define an analyzer that gets applied to a single opinion. 
#You may optionally include code to deal with multiple opinions in a file, including a flattening rule and a list of File names to exclude.
#Way at the bottom of this file are the handlers that apply the function

from handlers import prompt, queuer
from collections import Counter 
from bs4 import BeautifulSoup #for parsing our text files
import re

# TESTING REWRITING
# To load an opinion
# document_path =  "/Users/brianlibgober/Box Sync/Backup/Justia2/2000/79 New York v. Hill, 528 U.S. 110/79 New York v. Hill, 528 U.S. 110.txt"
# f = open(document_path,"r")
# soup = BeautifulSoup(f)



############# EDIT HERE #################

########## Helpers

def evacuate(string):
    disclaimer = "Official Supreme Court case law is only found in the print version of the United States Reports\. Justia case law is provided for general informational purposes only, and may not reflect current legal developments, verdicts or settlements\. We make no warranties or guarantees about the accuracy, completeness, or adequacy of the information contained on this site or information linked to from this site\. Please check official sources\."
    string = re.sub(disclaimer,"",string,count=0)
    string = string.lower()
    return string


########## MAIN FUNCTIONS
#analyzes a single opinion in some way. The input is an "open file" in read mode. Almost any information you could want about the opinion is accessible in its name.
#Analyzer must return a list of tuples (list of pairs to use default flattener)
def analyzer(doc):
    
    #Parse HTML into beautiful soup
    soup = BeautifulSoup(doc)
    
    #Extract opinion
    opinion_html = soup.find(id="opinion")
    
    #If fail to get any text print a warning
    if opinion_html == None:
        print("Was not able to extract any text from " + doc.name + " I will try to move on")
        opinion_html = ""
    
    #Convert Opinion HTML to String
    opinion = opinion_html.get_text(" ",strip=True)
    
    #Expel materials that are not actually part of opinion (e.g. disclaimers, information about parties, docket no.)
    #Also fixes strings
    #opinion = evacuate(opinion) 
    
    #
    # A citation looks like Reporter (i.e. book name), page citation, then year
    #
    
    #container to hold the reporter strings, to check what each does view https://www.debuggex.com/. 
    reporters = []
    reporters.append(ur"[0-9]{1,3}\s*[uU][.\s]*[sS][.\s]*") #modern, e.g. 591 U.S. 
    reporters.append(ur"[0-9]{1,3}\s*[sS][.\s]*[cC][tT][.\s]*") #modern2, e.g. 47 S.Ct. Supreme Court Reporter, should be redundant
    reporters.append(ur"[0-9]{1,3}\s*[wW]al?l?a?c?e?[.\s]*") #Wallace e.g. 31 Wall. or various deviant forms
    reporters.append(ur"[0-9]{1,3}\s*[bB]la?c?k?[.\s]*") #Black, e.g. 1 Black
    reporters.append(ur"[0-9]{1,3}\s*[hH]ow?a?r?d?[.\s]*") #Howard
    reporters.append(ur"[0-9]{1,3}\s*[pP]et?e?r?s?[.\s]*") #Peters
    reporters.append(ur"[0-9]{1,3}\s*[wW]he?a?t?o?n?[.\s]*") #Wheaton
    reporters.append(ur"[0-9]{1,3}\s*[cC]ra?n?c?h?[.\s]*") #Cranch 
    reporters.append(ur"[0-9]{1,3}\s*[dD]al?l?a?s?[.\s]*") #Dallas
    #combination of U.S. with the other reporters in parentheses is possible 66 U.S. (1 Wall.), 66 U.S. (1 Black), etc.
    reporters = reporters + map(lambda x: reporters[0]+"[\(]?"+x+"[\)]?",reporters[2:])
    #reorder the first element to the end since it's part of things we will match
    reporters.append(reporters.pop(0))
    pages = ur"\s*[_0-9]{1,3}[\s,\-\–\—\―]*[_0-9]{0,3}[\s,\-\–\—\―]*[_0-9]{0,3}" #pages 303, 312-3
    year = ur"\s*(?:[\(]?[0-9]{1,4}[\)]?)?" #year
    #combine the reporters with pages and year to form a bunch of regexes
    particular_regexes = map(lambda x: x + pages + year,reporters)
    #combine the regexes into a singleton using |
    search_expression = reduce(lambda x, y: x + "|" + y,particular_regexes)

    #Divide the text of the opinion into a list of words and then count them
    tabulation = Counter(re.findall(search_expression),unicode(opinion)))
    
    #Throw away everything that occurs only once in the opinion
    tab = {key:value for key,value in tabulation.items() if value>1}

    return tab.items()

#Optionally include a list of headers to add
headers = []

#Optionally include a rule for dealing with the possibility of multiple documents in a single folder. 
#Input will be a list of list of tuples. Output must be a list of tuples.
#Default will be to combine all the files not found in the skip list.
flattening_rule = None

#Optionally include a list of opinion names to skip, such as Syllabus.txt
skip_list = []








#################################################################
########### Should not neeed to touch this
#################################################################



# Prompt returns an array like [Write Object,Parent Directory,Start Year,End Year, First Case, Last Case]
# Defaults will be [File Object "results.tsv",".",1800,2015,1,None]
initial_values = prompt()

#queuer takes the analyzer and applies it to a file within an opinion's folder, returning a list of words and counts. It then repeats this over the year range required.
#Since there are potentially several files in a folder, it takes an optional flattening rule, but by default all the frequency counts will be combined
#We also allow for a set of file names to exclude, for example we may not want to apply analyzer to files with names like "Syllabus.txt" 
queuer(analyzer,headers,flattening_rule,skip_list,initial_values[0],initial_values[1],initial_values[2],initial_values[3],initial_values[4],initial_values[5])

