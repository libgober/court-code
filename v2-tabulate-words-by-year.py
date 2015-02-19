#Gets a word from the word-list database, which is unique and ordered sequentially
#Tabulates all entries for a given year, moves to next

import pyodbc #for MySQL interaction
import sys

#This function checks for the existence of an ID and a word associated with it
def get_word(id):
    
    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')

    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
    #add the counts to MySQLSELECT word FROM word_count WHERE id = 1
    word = cursor.execute("SELECT word FROM word_list WHERE id = ?",id).fetchone()

    return word

def tabulate(input,id):
    
    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')
    
    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
    #execute tabulate command
    cursor.execute("""INSERT INTO word_totals_by_year (word, word_list_id, year, total)
SELECT ?, ?, bdl_opinion_cat.year_decided, sum(word_count.`frequency`)
FROM word_count
INNER JOIN bdl_opinion_cat
ON bdl_opinion_cat.case_id = word_count.case_id
WHERE word = ?
GROUP BY bdl_opinion_cat.year_decided, word_count.word
order by bdl_opinion_cat.year_decided""",input,id,input)
    
    #commit the connection to save these values
    cnxn.commit()
    
end  = 194959
for id in xrange(int(sys.argv[1]),end,1):
    print "Starting on ID Number " + str(id)
    word = get_word(id)
    if word == None:
        print "Yikes Missing Word!"
        continue 

    print "Adding " + word[0] + " to Database!"                       
    tabulate(word[0],id)
    print(str(id) "- word list id has been added")
