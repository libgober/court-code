This is a brief explanation of the various text processing scripts and what their intended purpose is.

Processor-(1 and up) - Takes an opinion, counts the number of words occuring in it, and then spits out the opinion name and the word count, along with some other useful metadata. Versions 1 through 3 (of which 3 is best) connect to a SQL database to do this. In an effort to improve performance, Version 4 dumps the contents into a TSV file rather than connecting to a database. The reason to think this will improve speed is that running multiple parallel processes is a better idea with TSVs than MySQL, and also connecting to the SQL server is probably slower than writing to a file. 
	
	Versions 1-3 require customization to the SQL database in 	question.
	
	Version 4 takes as command line input the place to save the 	files.  
	
Tabulate Words by Year (V1 and up) - Interacts with a SQL database containing a list of unique words to come up with how many time each word occurs per year.