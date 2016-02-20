# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:37:30 2015

@author: Administrator
"""

"""
A simple script that demonstrates how we classify textual data with sklearn.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from numpy import array

#read the reviews and their polarities
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


rev_train,pol_train=loadReviews('Yelpreviews1.txt')
rev_test,pol_test=loadReviews('D:/testFile4.txt')


#count the number of times each term appears in a document and transform each doc into a count vector
counter = CountVectorizer(analyzer='word',ngram_range= (1,2),min_df=0,max_df=0.5)
counts_train = counter.fit_transform(rev_train)

#transform the counts into the tfidfd format. http://en.wikipedia.org/wiki/Tf%E2%80%93idf
transformer = TfidfTransformer()
transformed_train = transformer.fit_transform(counts_train)


#apply the same transformation on the test datqs
counts_test=counter.transform(rev_test)
transformed_test=transformer.transform(counts_test)

#make ane empty model
classifier1=LogisticRegression()
classifier2= MultinomialNB(alpha=0.5,class_prior=None,fit_prior=False)
classifier3=LinearSVC()
classifier4=KNeighborsClassifier(n_neighbors=10,weights='distance')
#fit the model on the training data
classifier1.fit(transformed_train,pol_train)
classifier2.fit(transformed_train,pol_train)
classifier3.fit(transformed_train,pol_train)
classifier4.fit(transformed_train,pol_train)

pred1=classifier1.predict(transformed_test)
pred2=classifier2.predict(transformed_test)
pred3=classifier3.predict(transformed_test)
pred4=classifier4.predict(transformed_test)



majorityDecision=[] #will hld the majority label (0/1) for each testing point
correct=0
for i in range(len(rev_test)):#for each testing point
    majority=1    
    if pred2[i]+pred3[i]+pred4[i]<2:majority=0 # if the sum is less than 2, then the majority label has to be 0
    majorityDecision.append(majority)
    
    if majority==pol_test[i]:correct+=1
#get the accuracy on the test data
print 'Logreg'
print 'ACCURACY:\t',classifier1.score(transformed_test,pol_test)
#print 'PREDICTED:\t',classifier1.predict(transformed_test)
#print 'CORRECT:\t', array(pol_test)

print 'Bayes'
print 'ACCURACY:\t',classifier2.score(transformed_test,pol_test)
#print 'PREDICTED:\t',classifier2.predict(transformed_test)
#print 'CORRECT:\t', array(pol_test)

print 'Linear SVC'
print 'ACCURACY:\t',classifier3.score(transformed_test,pol_test)
#print 'PREDICTED:\t',classifier3.predict(transformed_test)
#print 'CORRECT:\t', array(pol_test)

print 'KNN'
print 'ACCURACY:\t',classifier4.score(transformed_test,pol_test)

print 'MAJORITY:\t'
#print 'CORRECT:\t', array(pol_test)
print 'ACCURACY', correct*1.0/len(pol_test)






