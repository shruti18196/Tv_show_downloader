#!/usr/bin/python3
import re
import bs4
import urllib.request as ur
import requests
import time
import threading

header= { 'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}

def func_util(url,url_orig,counter,ep_list,did_2,url_seas,url_ep):
    first_abc='h/'
    got=False
##    print("func util called")
    
    ep_flag=0
    flag0=0
    flag1=0
    flag2=0
    k=0
    
    while(True):
          if(first_abc[-1] is not '/'):                           #to check !=end of dir (termination of dir)
                    got=True
##                    print("first_abc")
                    break  

          try:
              req = requests.get(url,headers=header,timeout=10)
##              print(url)
              if(req.status_code==200):
                  soup=bs4.BeautifulSoup(req.text,'xml')
            
                  for url_1 in soup.find_all('a'):
##                    print("in for")
                    used=0
                    can_2=0
                    flag1=0
                    abc=url_1.get("href")
                    
                    abc_meta=url_1.text                                # abc_meta to check the url.text matched with seas list or not
                    
                    a =re.findall(r"\-|\_|\s",abc_meta)
                    
                    for d in a:
                      abc_meta=abc_meta.replace(d,"")
                    

                    if(counter[0]==0 and flag0==0):
                       yo=0
                       j=0
##                       print("in counter[0]")
                       for j in url_seas:
                        if(j in abc_meta):
                          yo=1
                          counter[0]=1
                          used=1
##                          print("j in abc meta")
                          break

                       if(yo==1):
##                        print("yo=1")
                        if(abc_meta.find("/")>len(j)+2): #season 1 720p
##                            print("len more than season")
                            url+=abc
                            func_util(url,url_orig,counter,ep_list,did_2,url_seas,url_ep)
                            counter[0]=0
                            url=url_orig
                            continue
                        else:
##                            print("len equals season")
                            flag0=1
                            url+=abc
                            url_orig=url
                            can_2=1
                        
                     
                       else:
                           continue


                       

                    elif(counter[1]==0 and flag1==0):  #episode
##                       print("in counter[1]")
                       if(abc=='../'):
                         continue
                        
                       if (abc[-3:] == 'mkv' or abc[-3:] == 'mp4' or abc[-3:] == 'avi'): 
##                          print("in if mkv part")
                          j =url_ep

                          if(j in abc):
                              ep_list.append(url+abc)
                              ep_flag=1
                              flag1=0
                              continue
                          else:          #got some episodes
                              if(ep_flag==1 and did_2==1):
                                  used=1
                                  flag1=1
                              else:
                                  
                                   continue
                       else:      
                          if(abc[-1]=='/'):
##                             print("got here")
                             flag1=2
                           
                             

                    if(counter[2]==0 and flag2==0 and flag1==2 and can_2==0 ):
##                       print("in counter[2]")
                       url+=abc
                       flag1=0
                       did_2=1
                       func_util(url,url_orig,counter,ep_list,did_2,url_seas,url_ep)
                       url=url_orig
                       flag1=1
##                       print("original url:"+url)
                
                       continue
             
                    if(used==1):
                      got=True
                      break
                    else:
                      got=False

                   
                  if(got==False):
##                   print("not in this site")
                   break
             
                    
                  first_abc=abc
                  if(flag1==1):
                    break

              else :
                  pass
##                  print("req code !=200")
          except Exception as e:
              pass
##              print(str(e))
              break

    return(ep_list)
     

    
def func(url_seas,url_ep,i,lock,episode_file,shows):
        global header
        
##        print("func starts")
##        print("Thread {}".format(i))
        ep_list=[]
        for line in shows:
            did_2=0
            url=line.strip("\n")
            url_orig=url
##            print(url)
            
            counter=[0,0,0]
            got=False
            ep_list=func_util(url,url_orig,counter,ep_list,did_2,url_seas,url_ep)
        lock.acquire()
        for i in ep_list:
          if( 'farsi' in i or 'Farsi' in i):
              episode_file.write(i+' farsi'+"\n")
          else:
              episode_file.write(i+"\n")
        lock.release()
##        print(ep_list)
        
            



def final(season,ep):
    url_seas=['Season','season','S','s','season','Season']
    url_ep='E'
##    print(season,ep)
##    season=input("season ")
##    ep=input("ep ")
    url_seas[0]+=season
    url_seas[1]+=season
        
    if len(season) is 1 :
       season='0'+season

    if len(ep) is 1 :
       ep='0'+ep

    url_ep+=ep
##    print(url_ep)


    for i in range(2,len(url_seas)):
        url_seas[i]+=season

    url_seas.append(season)

##    print(url_seas)

    shows=open("matched_1.txt","r")
    episode_file=open("epis.txt","w")

    episode_file=open("epis.txt","a")
    lock=threading.Lock()
    thread=[]
    for i in range(6):
        t=threading.Thread(target=func, args=(url_seas,url_ep,i,lock,episode_file,shows))
        thread.append(t)


    start = time.time()
    for i in thread:
        i.start()
    for i in thread:
        i.join()
    episode_file.close()
    
    time_spend =time.time()-start
####    print("total time {} ".format(time_spend))
##    
####    print("end of it")

    shows.close()
    return "seasons episode done"


##final('1','1')



        
