#elimiante stopwords from a list of 1 grams
from nltk.corpus import stopwords
import gzip
import

#load a file we want to clean
f = gzip.open





stop = stopwords.words('english')




#read row
#read until you hit a number and save all those words in a list
#if everythig in the list is in the list of stopwords then delte the row
#else nextrow