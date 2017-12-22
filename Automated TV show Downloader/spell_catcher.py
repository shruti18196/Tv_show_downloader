#!/usr/bin/python3
######### module for searching ###########
import urllib.parse as ub
import urllib as u
import requests
import time
from bs4 import BeautifulSoup

header = { 'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}


def LCS(show,A):
   show=show.lower()
   A=A.lower()

   show=show.replace(" ","")
   A=A.replace(" ","")
   n=len(show)
   m=len(A)
##   print(show)
##   print(A)
##   print(n,m,"\n\n")
   n=n+2
   m=m+2
   arr=[[0]*(n) for i in range(m)]  

  
   for i in range(m-1):
     for j in range(n-1):
##        print(i,j)
        if i==0 or j==0:
          pass
        elif(show[j-1]==A[i-1]):
          arr[i][j]=arr[i-1][j-1]+1
        else:
          arr[i][j]=max(arr[i-1][j],arr[i][j-1])
   
##   for i in range(m-1):
##     print("\n")
##     for j in range(n-1):
##       print(arr[i][j],end=" ")
##   print(arr[m-2][n-2])
   return arr[m-2][n-2]


    
def spell(show):
  show2 = show
  show="TV series "+show+" IMDB"
  show =ub.urlencode({'q': show})# results q=abc+defg replace spaces by + and append q= to the starting of the string
##  print(show)
  url = 'https://www.bing.com/search?'+show
##  print(url)
  abc= []
##  n=show.count(" ")
  for start in range(1):
      req=requests.get(url,headers=header)
      if( req.status_code == requests.codes.ok):      
          soup=BeautifulSoup(req.text,'lxml')            
          for url in soup.find_all('a'):
            if("1" == url.text):
               break
            if("www.imdb.com/title/" in url.get('href')):
              corrected=''
              for s in url.text :
                if( s!='('):
                        corrected+=s
                else :
                        break
##              print(corrected)
              abc.append(corrected)
##          print(abc)
          max_match=0
          k='a'*10000
          for i in abc:
            r=LCS(show2,i)
##            print(r,max_match)
            if(r>max_match):
               k=i
               max_match=r
            elif(len(k)>len(i) and r==max_match):
                k=i
                max_match=r
            
          return(k)
      else:
         pass
##          print("503")
      

