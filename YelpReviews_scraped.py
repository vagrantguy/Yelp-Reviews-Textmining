# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 09:39:31 2015
Mid-Term Yelp

@author: BIA660A - Group7

Part1: Get links of each restaurant
"""
#import the two libraries we will be using in this script
import urllib2,re

#make a new browser, this will download pages from the web for us. This is done by calling the 
#build_opener() method from the urllib2 library
browser=urllib2.build_opener()

#desguise the browser, so that websites think it is an actual browser running on a computer
browser.addheaders=[('User-agent', 'Mozilla/5.0')]


#number of pages you want to retrieve (remember: 10 restaurants per page)
#pagesToGet=2

#create a new file, which we will use to store the links to the restaurants. 
fileWriter=open('Yelp.txt','w')

pagesToGet=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
#
rest_freq=dict()
#for every number in the range from 1 to pageNum+1  
for page in pagesToGet:
    
    print 'processing page :', page
    
    #make the full page url by appending the page num to the end of the standard prefix
    url='http://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY&start='+str(page-1)+'0'
    #http://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY&ns=1
    #http://www.yelp.com/search?find_desc=Restaurants&find_loc=Jersey+City%2C+NJ&start=
    
    #use the browser to get the url and use it in the html
    myHTML=browser.open(url).read()    

    unique=set()#remember unique usernames	
    RestMatches=re.finditer('<a class="biz-name" href="/biz/(.*?)"',myHTML)#get all the matches
    
    
    for RestMatch in RestMatches:
        Restname=RestMatch.group(1) # get the username
        if Restname in rest_freq:
            rest_freq[Restname]=rest_freq[Restname]+1
        else:
            rest_freq[Restname]=1
    
    page+=1    
         
for Restname in rest_freq:
    if rest_freq[Restname]==1:
        fileWriter.write('http://www.yelp.com/biz/'+Restname+'\n') #write the results
fileWriter.close()#close the file.


"""
Part 2: Get the text, date and stars in the reviews of these restaurant
"""
fileWriter1=open('Yelpreviews.txt','w')
fileReader1=open('Yelp.txt')
pageofReview=2
Restaurant=1
posCount=0
negCount=0
posGet=3000
negGet=3000
for line in fileReader1: # this syntax allows us to read the file line-by-line
        link=line.strip() # .strip() removes white spaves and line-change characters from the beginning and end of a string
     
        nextPage=1
        
        print 'Restaurant: ',Restaurant
        
        while nextPage<pageofReview+1:#for every number in the range from 1 to pageNum+1  
            print 'processing page :',nextPage, '\t','40 reviews per page'
            url1 = link+'?start='+str((nextPage-1)*4)+'0' #make the full page url by appending the page num to the end of the standard prefix
       
            #use the browser to get the url and read it in html format.
            myHTML1=browser.open(url1).read()    
            
            #get the name of restaurant that the review is about
            #match=re.search('<meta property="og:title" content="(.*?)">',myHTML1) 
            #title=match.group(1)
            
            #get the ID of restaurtant that the review is about
            #IDmatch=re.search('data-hovercard-id="(.*?)"',myHTML1)
            #ID=IDmatch.group(1)           
     
            #get all the matches
            reviewMatches=re.finditer('<div class="review-wrapper">(.*?)<div class="review-footer clearfix">', myHTML1,re.S)
        
            revCount=0
           
            for rmatch in reviewMatches:
                entry=rmatch.group(1) # get the part which include the information looked for
                           
  
                #get the stars rating of the review
                stars=float(re.search('title="(\d\.\d) star rating', entry).group(1))
                if stars > 3 and posCount<posGet:
                    result = "1"
                    textMatch=re.search('description" lang="en">(.*?)</p>', entry)     
                    text=textMatch.group(1)
                    posCount+=1
                   
                elif stars <3 and negCount<negGet:
                    result = "0"
                #else: result
                    textMatch=re.search('description" lang="en">(.*?)</p>', entry)     
                    text=textMatch.group(1)
                    negCount+=1
                else:
                    continue
                        
                
                    
                #if result == "0" or "1":    
                """if stars > 3:
                    result = "1"
                else:
                    result = "0"
                 """   
                
                        
                #if stars==5 or 1:
                
                #get the date on which the review was submit
                #DateMatch=re.search('"datePublished" content="(.*?)">',entry)    
                #date=DateMatch.group(1)
                
                textnew=text.replace("&#39;","'").replace("<br><br>"," ").replace("<br>"," ").replace("&#34;","\"").replace('&amp;','&')

                revCount+=1
        
                #fileWriter1.write(title+'\t'+ID+'\n'+date+'\n'+str(stars)+'\n'+text+'\n\n')
                fileWriter1.write(textnew+'\t'+result+'\n')
             
             #When there is any problem about getting data on a review, the program needn't reload from the begin.
            if revCount==0:
                print 'FAIL'  
                #nextPage+=1    
                #Restaurant+=1
                continue
        
            nextPage+=1    
        Restaurant+=1
fileWriter1.close()#close the file. 
