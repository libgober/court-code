#
# This program loops through the ids of the database and adds 
#
#for i in set of id numbers in database:
#    check if i exists in table, if not move on #for example 19 doesn't exist
#    
#    check in destination table if i's word is already there
#    if already there: 
#        next i
#    else:
#        query the database and get the big sum bad boy and add that to destination table
#        next i
#        
#        

import pyodbc #for MySQL interaction

#This function checks for the existence of an ID and a word associated with it
def get_word(id):
    
    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')

    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
    #add the counts to MySQLSELECT word FROM word_count WHERE id = 1
    storage = cursor.execute("SELECT word FROM word_count WHERE id = ?",id).fetchone()

    return storage

def check_destination(input):
    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')

    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
    #add the counts to MySQLSELECT word FROM word_count WHERE id = 1
    storage = cursor.execute("SELECT word FROM `word_totals_by_year` where word=? LIMIT 1",input).fetchone()

    return storage

def tabulate(input):
    
    #Create connection object to MYSQL database
    cnxn = pyodbc.connect('DSN=Court')
    
    #Create cursor object for interaction with connection
    cursor = cnxn.cursor()
    
    #execute tabulate command
    cursor.execute("""INSERT INTO word_totals_by_year (word, year, total)
SELECT ?, bdl_opinion_cat.`year_decided`, sum(word_count.`frequency`)
FROM word_count
INNER JOIN bdl_opinion_cat
ON bdl_opinion_cat.`case_id` = word_count.`case_id`
WHERE word = ?
GROUP BY bdl_opinion_cat.`year_decided`, word_count.`word`
order by bdl_opinion_cat.`year_decided`""",input,input)
    
    #commit the connection to save these values
    cnxn.commit()

for id in xrange(415,418,1):
    print "Starting on ID Number " + str(id)
    word = get_word(id)
    if word == None:
        print "Yikes Missing Word!"
        continue 
        
    if check_destination(word[0]) != None:
        print "Already Added " +  word[0]
        continue
        
    tabulate(word[0])
    print "Adding " + word[0] + " to Database!" 
        