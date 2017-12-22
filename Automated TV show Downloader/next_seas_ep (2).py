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
      with open('auto2.txt') as f:
          for line in f:
            if(show in line):
                  print(line)
                  print("Already registered")
                  return True
          return False

  def next_ep_seas(self,show,f):

    n=show.count(" ")
    print(n)
    show1=show
    show=show.replace(" ","-")
    print(show)
    flag=0
    self.url = "https://next-episode.net/site-search-"+show+".html"
    print(self.url)   
    req=requests.get(self.url,headers=self.header)
    if( req.status_code == requests.codes.ok):    
          soup1=BeautifulSoup(req.text,'lxml')
          yup=soup1.find('h1')
          print(str(yup))
          if('Searching' in str(yup)):
            for url in soup1.find_all('a'):
##              print(url.get("href").split('/')[-1])

              if(show.lower() == url.get("href").split('/')[-1] and url.get("href").split('/')[-1].count("-")==n):
##                print(url.get("href"))
                self.url="https://next-episode.net"+url.get("href")
                print(self.url)
                req=requests.get(self.url,headers=self.header)
                if( req.status_code == requests.codes.ok):    
                  soup1=BeautifulSoup(req.text,'lxml')
                flag=1;
                  
                break
              
          try:
         

            for episode in soup1.find_all(id='next_episode'):
              flag1=1
              episode = episode.text.split('\n')[3]+'\t'+episode.text.split('\n')[8]+episode.text.split('\n')[9]
              episode=episode.split('\t')
              print(episode)
              print(episode[0]+'\n'+episode[1]+'\n'+episode[4])
              

            if(flag1==1):
              print("flag1")
              f.write(show1+"+"+episode[0]+"+"+episode[1]+"+"+episode[4]+"+")

            else:
              print("Sorry next seas and ep info not found")

       

          except:
              print("Sorry next seas and ep info not found")
            
  def date_time(self,show,f):
    n=show.count(" ")
    print(n)
    show=show.replace(" ","+")
    print(show)
    
    self.url = "https://www.episodate.com/search?q="+show
    print(self.url)
    req=requests.get(self.url,headers=self.header)
    if( req.status_code == requests.codes.ok):      
        soup=BeautifulSoup(req.text,'lxml')            
           
        try:
            flag=0
            yo=soup.findAll('h1',{'class':'title'})
            print(str(yo))
            if('Searching' in str(yo)):
               print("Searching")
               for i in range(1,4):
                    print(i)             
                    for url in soup.find_all('a'):
##                        print(url.get("href"))
                        if("tv-show" in url.get("href") and url.get("href").split('/')[-1].count("-")==n):
                            print(url.get("href").split('/')[-1])
                            self.url="https://www.episodate.com"+url.get("href")
                            print(self.url)
                            req=requests.get(self.url,headers=self.header)
                            if( req.status_code == requests.codes.ok):      
                                soup=BeautifulSoup(req.text,'lxml')            
        
                            
                            flag=1
                            break
                        
                       
                    if(flag==1):
                        break
                    self.url = "https://www.episodate.com/search?q="+show+"&page="+str(i+1)
                    print(self.url)
                    req=requests.get(self.url,headers=self.header)
                    if( req.status_code == requests.codes.ok):      
                         soup=BeautifulSoup(req.text,'lxml')            
        
            
            date = soup.findAll('div' , {'class','countdown'})
            print(str(date).split("\"")[3])
        
            if ( '0' in (str(date).split("\"")[3])) :
##                print("came here")
                print((str(date).split("\"")[3].strip("GMT")))
                f.write(str(date).split("\"")[3]+'\n')

                print("found and registered")
            else:
                print("Sorry!! Either show has ended or Server has no record")
       
        

        except Exception as e:
                print("exception")
                print("Sorry!! Either show has ended or Server has no record")



p=pro()
show="legends of tomrow"
show = sp.spell(show).strip(' ')

f= open('auto2.txt','a+')    

print(show)
if(p.check(show)==False):    # what if not created initially

  p.next_ep_seas(show,f)
  p.date_time(show,f)   
  f.close()


