#!/usr/bin/python3
######### module for nextepisode ###########
import urllib.parse as ub
import urllib as u
import requests
import time
import spell_catcher as sp
from bs4 import BeautifulSoup


   
class pro:

  def __init__(self):
    self.url = ''
    self.url2 = ''
    self.header = { 'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}

  def check(self,show):
      with open('automate2.txt') as f:
          for line in f:
            if(show in line):
                  print(line)
                  return True
          return False

        
  def New_episode(self,show):
    show = sp.spell(show)
    show2 = show
    show=show+"Next-Episode"
    show =ub.urlencode({'q': show})# results q=abc+defg replace spaces by + and append q= to the starting of the string
##    print(show)
    self.url = 'https://www.bing.com/search?'+show
##    print(self.url)
    flag=0
    f= open('automate2.txt','a+')    
    req=requests.get(self.url,headers=self.header)
    if( req.status_code == requests.codes.ok):      
        soup=BeautifulSoup(req.text,'lxml')            
        for url in soup.find_all('a'):
          if("https://www.episodate.com/" in url.get("href")):
##            if(url.get("href").split('/')[-1].lower()==show.lower()):
##              print(url.get("href"))
              self.url=url.get("href")
              flag+=1

          if(flag==2):
              break
            
          if ("https://next-episode.net/" in url.get("href") and flag==0):
##            print(url.get("href"))
            self.url2=url.get("href")
            flag+=1

    req = requests.get(self.url,headers = self.header)
    req2 = requests.get(self.url2,headers = self.header)
    value = self.check(self.url.split('/')[-1])
    if ( value == True):
        return "Already in the list, Sir!!"
    else:
      if(req.status_code == requests.codes.ok):      
          soup=BeautifulSoup(req.text,'lxml')
          soup2 =BeautifulSoup(req2.text,'lxml')
          try:
            for episode in soup2.find_all(id='next_episode'):
                episode = episode.text.split('\n')[8]+episode.text.split('\n')[9]
                episode=episode.split('\t')
##                print(episode)
            date = soup.findAll('div' , {'class','countdown'})
            if ( '0' in (str(date).split("\"")[3])) :
##                print((str(date).split("\"")[3].strip("GMT")))
                f.write(self.url.split('/')[-1] +' + '+str(date).split("\"")[3]+' , '+episode[0]+', '+episode[3]+'\n')
##                print("found and registered")
                return "found and registered"
            else:
##                print("Sorry!! Either show has ended or Server has no record")
                return "Sorry!! Either show has ended or Server has no record"
          except Exception as e:
##                print("Sorry!! Either show has ended or Server has no record")
                return "Sorry!! Either show has ended or Server has no record"
    f.close()



