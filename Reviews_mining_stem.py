# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 01:31:42 2015

@author: Jessica
"""
import os
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

from sklearn import cross_validation
from numpy import array
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
#import pylab as pl

os.chdir('D:\BIA\BIA660Web Analytics\HOMEWORK\FINAL PROJECT')
os.getcwd()

stemmer1=SnowballStemmer("english",ignore_stopwords=False)
stemmer2=PorterStemmer()

def stemming(sentence):
    try:
        sentence=re.sub(words[i],stemmer1.stem(words[i]),sentence)
    except UnicodeDecodeError:
        pass
    return sentence
        
def loadReviews(fname):
    
    reviews=[]
    polarities=[]
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')    
        reviews.append(review.lower())    
        polarities.append(int(rating))
    f.close()

    return reviews,polarities

rev_train,pol_train=loadReviews('Yelpreviews-142915-3V2.txt')
rev_test,pol_test=loadReviews('D:/testFile4.txt')

def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex
#load the positive and negative lexicons

posLex=loadLexicon('positive-words.txt')
negLex=loadLexicon('negative-words.txt')
stopLex=loadLexicon('stop-words.txt')

posList=['try','authentic','prompt','gem','sublime','impressed','appreciate','remarkable','heavenly','delicate','quickly',\
         'unique', 'friendly','homemade','a big fan','a huge fan','out of this world','no better','not bad','not disappointed','5 star',\
         'hats off','must try','only complaint','home made']
negList=['disappointed','disappoint','stinks','salty','inedible','shoot','tiny','unreasonably','forever','impolite','barely','not really',\
         'not exactly','never been','in need of','never go back','never recommend','not be returning','never again','not return','never going back',\
         'way too','stay away','not even','cost a fortune','let me down','let you down','over rated','no longer','used to be','never been','couldn’t believe','unseasoned']
rev_test2=[]
rev_train2=[]

#special phrase replacement
for review in rev_test :
    sent1=re.sub('\d+\$','xaaax',review)
    sent1=re.sub('\$\d+','xaaax',sent1)
    sent1=re.sub('\d+ minutes','xbbbx',sent1)
#define pos and neg
    for i in range(0,25):
        sent1=re.sub(posList[i],'amazing',sent1)
    for i in range(0,33):
        sent1=re.sub(negList[i],'terrible',sent1)

#escape sentiment   
#    sent1=sent1.translate(None,string.punctuation) 

    words=sent1.translate(None,string.punctuation).split(' ')
    n=len(words)
    for i in range(0,n-1):
        if words[i] in ["no","not","never","isn't","wasn't","terrible"]:
            if words[i+1] in posLex:
               sent1=re.sub(words[i],'',sent1)
               sent1=re.sub(words[i+1],'terrible',sent1)
            if words[i+1] in negLex:
               sent1=re.sub(words[i],'',sent1)
               sent1=re.sub(words[i+1],'amazing',sent1)
        sent1=stemming(sent1)
   
    rev_test2.append(sent1)
print 'done #0'
#special phrase replacement

for review in rev_train :
    sent2=re.sub('\d+\$','xaaax',review)
    sent2=re.sub('\$\d+','xaaax',sent2)
    sent2=re.sub('\d+ minutes','xbbbx',sent2)
#define pos and neg
    for i in range(0,25):
        sent2=re.sub(posList[i],'amazing',sent2)
    for i in range(0,33):
        sent2=re.sub(negList[i],'terrible',sent2)
    

    words=sent2.translate(None,string.punctuation).split(' ')
    n=len(words)
    for i in range(0,n-1):
        if words[i] in ["no","not","never","isn't","wasn't","terrible"]:
            if words[i+1] in posLex:
               sent2=re.sub(words[i],'',sent2)
               sent2=re.sub(words[i+1],'terrible',sent2)
            if words[i+1] in negLex:
               sent2=re.sub(words[i],'',sent2)
               sent2=re.sub(words[i+1],'amazing',sent2)
        sent2=stemming(sent2)

    rev_train2.append(sent2)    

print 'done #1'

#count the number of times each term appears in a document and transform each doc into a count vector
counter = CountVectorizer(analyzer='word',ngram_range=(1,2),min_df=0,max_df=0.5)
counts_train = counter.fit_transform(rev_train2)
#transform the counts into the tfidfd format. http://en.wikipedia.org/wiki/Tf%E2%80%93idf
transformer = TfidfTransformer()
transformed_train = transformer.fit_transform(counts_train)
#apply the same transformation on the test datqs
counts_test=counter.transform(rev_test2)
transformed_test=transformer.transform(counts_test)

#kf=cross_validation.KFold(transformed_train.shape[0],n_folds=4)



#clf=[LogisticRegression(),KNeighborsClassifier(n_neighbors=8,weights='distance'),MultinomialNB(alpha=0.5,class_prior=None,fit_prior=False),LinearSVC(),BaggingClassifier()]
clf1=LogisticRegression()
clf2=MultinomialNB(alpha=0.1,class_prior=None,fit_prior=True)
clf3=LinearSVC(dual=False)
#clf4=KNeighborsClassifier(n_neighbors=10,weights='distance')
#clf5=SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=None)
#fit the model on the training data
clf1.fit(transformed_train,pol_train)
clf2.fit(transformed_train,pol_train)
clf3.fit(transformed_train,pol_train)
#clf4.fit(transformed_train,pol_train)
#clf5.fit(transformed_train,pol_train)

pred1=clf1.predict(transformed_test)
pred2=clf2.predict(transformed_test)
pred3=clf3.predict(transformed_test)
#pred4=clf4.predict(transformed_test)
#pred5=clf5.predict(transformed_test)

majorityDecision=[] #will hld the majority label (0/1) for each testing point
correct=0
for i in range(len(rev_test)):#for each testing point
    majority=1    
    if pred1[i]+pred2[i]+pred3[i]<2:majority=0 # if the sum is less than 2, then the majority label has to be 0
    majorityDecision.append(majority)
    
    if majority==pol_test[i]:correct+=1
   
print 'Logreg'
print 'ACCURACY:\t',clf1.score(transformed_test,pol_test)
#print 'PREDICTED:\t', pred1
#print 'CORRECT:\t', array(pol_test)
#print 'Cross Validation', cross_validation.cross_val_score(clf1,transformed_train,pol_train,cv=kf)



print 'Bayes'
print 'ACCURACY:\t',clf2.score(transformed_test,pol_test)
#print 'PREDICTED:\t',pred2
#print 'CORRECT:\t', array(pol_test)
#print 'Cross Validation', cross_validation.cross_val_score(clf2,transformed_train,pol_train,cv=kf)



print 'Linear SVC'
print 'ACCURACY:\t',clf3.score(transformed_test,pol_test)
#print 'PREDICTED:\t',pred3
#print 'CORRECT:\t', array(pol_test)
#print 'Cross Validation', cross_validation.cross_val_score(clf3,transformed_train,pol_train,cv=kf)

#print 'KNN'
#print 'ACCURACY:\t',clf4.score(transformed_test,pol_test)
#print 'PREDICTED:\t',clf4.predict(transformed_test)
#print 'CORRECT:\t', array(pol_test)
#print 'Cross Validation', cross_validation.cross_val_score(clf4,transformed_train,pol_train,cv=kf)

#print 'SGD'
#print 'ACCURACY:\t',clf5.score(transformed_test,pol_test)
#print 'PREDICTED:\t',clf4.predict(transformed_test)
#print 'CORRECT:\t', array(pol_test)
#print 'Cross Validation', cross_validation.cross_val_score(clf4,transformed_train,pol_train,cv=kf)


print 'MAJORITY:\t'
#print 'CORRECT:\t', array(pol_test)
print 'ACCURACY', correct*1.0/len(pol_test)
