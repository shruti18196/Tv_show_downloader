#!/usr/bin/python3
import re
import bs4
import urllib.request as ur
import requests
import time
import threading
import spell_catcher

header = { 'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}


def func(name,show,urlf,lock,show_file,w):
    global header

##    print(name)
##    print("in {}".format(name)+"\n")

    global count
    count_1=0
    show_file=open('matched_1.txt','a')

    for line in w:
      url=line.strip("\n")
##      print(url)

      try:
            req = requests.get(url,headers = header,timeout=10)
##            print(req.status_code)
            if(req.status_code==200):
              soup=bs4.BeautifulSoup(req.text,"lxml")
              abc=''
              for url in soup.find_all('a'):
                abc = url.text
##                print(abc)
                k=urlf+'.*'
                matched=re.search(r'(?i)'+k,abc)
##                print(matched)


                if  matched is not None:
                  abc_href=url.get("href")
                  f_url=line.strip("\n")+abc_href
##                  print(f_url)
                  with lock:
                    show_file.write(f_url)
                    show_file.write('\n')
                  
              count_1+=1
##              print("count_{} is:".format(name),count_1)

            else :
               pass
            
      except Exception as e:
          pass
##           print("in :"+name)
##           print(str(e)+'\n')

    
    


#making 3 threads:


def final(show):
    show_file=open("matched_1.txt","w")
    w=open("resource_1.txt","r")
    show = spell_catcher.spell(show)
##    print(show)
##    show=input("showname ")
    a = re.findall( r"\W",show)
    for d in a:
     show=show.replace(d," ")
##     print(show)

    words=show.split(" ")
##      print(words)
    l=len(words)
      
##      print(l)     
    str1='(?=.*?'
##    print(str1)
    str2=')'

    urlf=''
    if l==1:
      urlf+=(str1+'\\b'+words[0]+'\\b'+str2)

    else:
      for i in range(l):
        urlf+=(str1+words[i]+str2)



    lock=threading.Lock()
    
    thread=[]
    for i in range(3):
        t=threading.Thread(target=func, args=(str(i),show,urlf,lock,show_file,w))
        thread.append(t)


    start = time.time()
    for i in thread:
        i.start()
    for i in thread:
        i.join()

    show_file.close()

    
    end=time.time()
##    print("end:"+str(end))
##    print("time is:"+str(end-start))
    return "user_thread done"




    
