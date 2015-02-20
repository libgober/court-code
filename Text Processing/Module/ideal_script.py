#To create a script, you need to define an analyzer that gets applied to a single opinion. 
#You may optionally include code to deal with multiple opinions in a file, including a flattening rule and a list of File names to exclude.
#Way at the bottom of this file are the handlers that apply the function

from handlers import prompt, queuer
from collections import Counter 

#analyzes a single opinion in some way. The input is an "open file" in read mode. Analyzer must return a list of lists, i.e. something that looks like a table.
def analyzer(doc):
    return Counter(a=1)















#Optionally include a list of headers to add
headers = []

#Optionally include a rule for dealing with the possibility of multiple documents in a single folder. Default will be to combine all the files not found in the skip list.
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

