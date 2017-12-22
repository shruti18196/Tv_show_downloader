######### module for searching ###########
import urllib.parse as ub
import urllib as u
import requests
import time
from bs4 import BeautifulSoup

header = { 'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    
def spell(show):
  show2 = show
  show="TV show "+show+" IMDB"
  show =ub.urlencode({'q': show})# results q=abc+defg replace spaces by + and append q= to the starting of the string
##  print(show)
  url = 'https://www.bing.com/search?'+show
##  print(url)
  abc= []
  
  for start in range(1):
##      print ('########### page {} ############'.format(start+1))
##      time.sleep(2)
      req=requests.get(url,headers=header)
      if( req.status_code == requests.codes.ok):      
          soup=BeautifulSoup(req.text,'lxml')            
          for url in soup.find_all('a'):
            if("www.imdb.com/title/" in url.get('href')):
##              print(url.text)
              corrected=''
              for s in url.text :
                if( s!='('):
                        corrected+=s
                else :
                        break
##              print(corrected)
              return corrected
              break
            

      else:
          print("503")
      


