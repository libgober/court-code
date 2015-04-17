from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import os
import numpy as np
import scipy as sp 
import pickle
from numpy import *
####################################
####HELPER FUNCTIONS
####################################

def textify(doc):
    soup = BeautifulSoup(doc)    
    #Extract opinion
    opinion_html = soup.find(id="opinion")    
    #If fail to get any text print a warning
    if opinion_html == None:
        print("Was not able to extract any text from " + doc.name + " I will try to move on")
        opinion_html = ""    
    #Convert Opinion HTML to String
    opinion = opinion_html.get_text(" ",strip=True)
    return(opinion)
    
####################################
###########   Main       ###########
####################################
   
homedir = "/nfs/projects/b/blibgober/Courts"
corpus = [] 

end = 1000
iteration = 0
for i in os.listdir(homedir):
    if iteration == end:
        break
    os.chdir(homedir)
    if i in ['CSVs','Troublemakers']:
        continue
    else: 
        os.chdir(homedir + "/" + i)
        for j in os.listdir("."):
            print(j)
            for fname in os.listdir(homedir + "/" + i + "/" + j):
                f = open(homedir+"/"+i+"/"+j+"/"+fname)
                corpus.append(textify(f))
                iteration += 1

#create a vectorizer object
vectorizer = CountVectorizer(min_df=5)

#create the corpus
x_sparse = vectorizer.fit_transform(corpus)
vectorizer.get_feature_names()

x_dense = x_sparse.todense()

###########
#Critical Numbers
###############

K = 2 #number of topics
N = shape(x_dense)[1] # Number of words
D = shape(x_dense)[0] #number of documents
column_of_averages = x_dense.mean(axis=0)/sum(x_dense.mean(axis=0)) ###calculate column averages


##########################################################
############ Initialize Topic, Mixing DIstributions, and Assignments
##########################################################

#### Depreciated
###betas = vstack([column_of_averages for i in xrange(0,K)]) #create a matrix with average distribution for one k

#create a random matrix
betas = np.random.random(shape(x_dense)) 
for i in xrange(0,shape(betas)[0]):
    betas[i] = betas[i]/sum(betas[i])
    
##    
betas = matrix(betas)
#create a uniform chance of drawing each topic
thetas = np.matrix([1.0/K for i in xrange(0,K)]) 

#responsibility assignment
qs = np.random.random((K,shape(x_dense)[0]))
for d in xrange(D):
    top_value = max(qs[:,d])
    for k in xrange(K):
        if qs[k,d] == top_value:
            qs[k,d] = 1
        else:
            qs[k,d] = 0

#to test the initialization
sum(qs,axis=0)

qs = matrix(qs)


########################################################
################### Define Expectation Step ##############
########################################################

def multinomial_objective(beta,row,n):
    first = sp.special.gammaln(n+1) 
    second = - sum(map(lambda x: sp.special.gammaln(x+1),row))
    third = 0
    for i in xrange(shape(beta)[1]):
        if (row[0,i] is not 0) and (log(beta[0,i]) == (-inf)):
            third = -inf
        elif (row[0,i] is 0) and (log(beta[0,i]) == (-inf)):
            third = third + 0
        else:
            third = third + row[0,i]*log(beta[0,i])
    return(first+second+third)

def update_responsibility(betas,X):
    """
    Does some stuff
    """
    qs = []
    for d in xrange(D):
        doc = X[d,:]
        assignment = (-1,-inf) #create a temporary assignment that we will override
        for k in xrange(K):
            likelihood = log(thetas[0,k]) + multinomial_objective(betas[k,:],doc,sum(doc))
            if likelihood > assignment[1]:
                assignment = (k,likelihood)
            else:
                next
        entry = zeros((1,K))
        entry[0][assignment[0]] = 1
        qs.append(entry)
    return(matrix(vstack(qs)))
    
#qs = update_responsibility(betas,x_dense)
            

############################################
####  Maximization Step
############################################

def generate_new_betas():
    draw = np.random.random((1,N))
    return(draw/sum(draw))

#update the thetas given the qs
def update_thetas(qs):
    new_thetas =  matrix(qs)/D * matrix(ones((D,1)))
    #if there is ever a chance of never drawing a topic, reinitialize the mixing probabilities so that our newly generated topic has a fair shot.
    if any([new_thetas[0,i] == 0.0 for i in xrange(shape(new_thetas)[1])]):
        new_thetas= thetas = np.matrix([1.0/K for i in xrange(0,K)]) 
    return(transpose(new_thetas))

def update_betas(qs,x):
    summatrix = qs * x
    for i in xrange(shape(summatrix)[0]):
        if sum(summatrix[i]) == 0:
            summatrix[i] = generate_new_betas()
        else:
            summatrix[i] = summatrix[i] / sum(summatrix[i])
    return(summatrix)
    
########################################
###### Fit Model
################################
   
 #initialize thetas
thetas = update_thetas(qs)
 #initialize betas  
betas = update_betas(qs,x_dense) 
   
def overall_objective(betas,thetas,qs,x):
    objective = 0
    for d in xrange(D):
        bag = x[d]
        responsibility = qs[:,d]
    for k in xrange(K):
        if responsibility[k,0] == 1.0:
            pass
        else:
            contribution = log(thetas[0,k]) + multinomial_objective(betas[k],bag,sum(bag))
            objective = objective + contribution
    return(objective)
                
            
#evaluate objective
value_old = 0
value_new = overall_objective(betas,thetas,qs,x_dense)
diff = inf
while diff > 10**(-4):
    value_old = value_new
    #expectation step
    qs = update_responsibility(betas,x_dense)
    #maximization step
    thetas = update_thetas(qs)
    betas = update_betas(qs,x_dense)
    #updateobjective
    value_new = overall_objective(betas,thetas,qs,x_dense)
    #difference
    diff = abs(value_old - value_new)
    print("Difference in objective " + str(diff))
    
output = open('data.pkl', 'wb')
pickle.dump([qs,x_dense,betas,thetas], output)

