#!/usr/bin/python3
import curses
import time
import User_threads as ut
import seas_ep_qual_x265_new as seas
import threading
import downloader
import Next_epi,os
import interneton
import os
import signal


j=''
value=''
def check():
    global value
    std.refresh()
    std.addstr(1 ,1,"checking internet connection ...")
    while(value is not 'True' and value is not 'False'):
        std.addstr(1,len("checking internet connection ")+1,'.')
        std.refresh()
        time.sleep(0.4)
        std.addstr(1,len("checking internet connection ")+1,'..')
        std.refresh()
        time.sleep(0.4)
        std.addstr(1,len("checking internet connection ")+1,'...')
        std.refresh()
        time.sleep(0.4)
        std.addstr(1,len("checking internet connection ")+1,'')
        std.refresh()
        time.sleep(0.1)
    if(value == 'True'):
        pass
    else :
        std.clear()
        std.refresh()
        std.addstr(2, 1,'fail to connect to internet please try again later !!')
        std.getch()
        curses.endwin()
        os.kill(os.getppid(), signal.SIGHUP)
    
def icheck():
    global value
    value=interneton.internet_on()

def search(s_name,s_seasons,s_episode):
    global j
    k=(ut.final(s_name))
    j=(seas.final(str(s_seasons),str(s_episode)))
    std.refresh()

        
def search_tag():
    global j
    std.refresh()
    std.addstr(4 ,1,"Searching ...")
    while(j==''):
        std.addstr(4,len("searching ")+1,'.')
        std.refresh()
        time.sleep(0.4)
        std.addstr(4,len("searching ")+1,'..')
        std.refresh()
        time.sleep(0.4)
        std.addstr(4,len("searching ")+1,'...')
        std.refresh()
        time.sleep(0.4)
        std.addstr(4,len("searching ")+1,'')
        std.refresh()
        time.sleep(0.1)
    std.addstr(4, len("searching ")+1,'done')
##    print(os.stat("epis.txt"))
    if(os.stat("epis.txt")):
        std.addstr(6, 1 ,"Available in these kind of format :")
    
    

if __name__=="__main__":
    try :
        std =curses.initscr()
        std.clear()

        curses.echo()
        thread_i =threading.Thread(target=check,args=())
        thread_j =threading.Thread(target=icheck,args=())
        thread_i.start()
        thread_j.start()
        thread_i.join()
        thread_j.join()
        std.clear()
        s_name=b''
        while(s_name==b'' or s_name.decode("utf-8").strip(' ')==''):
            std.addstr(1 ,1,"Enter the Tv show name ")
            s_name = std.getstr(1,len("Enter the Tv show name ")+1,250)
            if(s_name==b''):
                std.clear()
                std.addstr(2,1,"please Enter the Showname")
                std.addstr(1,1,"Enter the Tv show name                           ")
                std.addstr(1,1,"Enter the Tv show name ")
        std.refresh()
        s_seasons=b''
        while(s_seasons==b'' or s_seasons.decode("utf-8").strip(' ')=='' or  (s_seasons.decode("utf-8").isdigit())==False):
            std.addstr(2,1, "Enter season as '02' or '2' ")
            s_seasons = std.getstr(2,len("Enter season as '02' or '2' ")+1,2)
            if(s_seasons==b'' or s_seasons.decode("utf-8").strip(' ')=='' or  (s_seasons.decode("utf-8").isdigit())==False):
                std.addstr(3,1,"please Enter season correctly")
                std.addstr(2,1,"Enter season as '02' or '2'       ")
                std.addstr(2,1,"Enter season as '02' or '2' ")
        std.addstr(3,1, " "*len("please Enter season correctly"))
        s_episode=b''
        while(s_episode==b'' or s_episode.decode("utf-8").strip(' ')=='' or s_episode.decode("utf-8").isdigit()==False):
            std.addstr(3,1, "Enter episode as '02' or '2' ")
            s_episode = std.getstr(3,len("Enter the episode as '02' or '2'")+1,2)
            if(s_episode==b'' or s_episode.decode("utf-8").strip(' ')=='' or s_episode.decode("utf-8").isdigit()==False):
                std.addstr(4,1,"please Enter episode correctly")
                std.addstr(3 ,1,"Enter the episode as '02' or '2'      ")
                std.addstr(3 ,1,"Enter the episode as '02' or '2' ")
        std.addstr(4,1, " "*len("please Enter episode correctly"))        
        thread_1=threading.Thread(target=search,args=(s_name.decode("utf-8"),s_seasons.decode("utf-8"),s_episode.decode("utf-8")))
        thread_2=threading.Thread(target=search_tag, args=())
        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()
        if(os.stat('epis.txt')):
            fp= open("epis.txt","r")
            count=8
            link=[]
            l=['720p','1080p','480p']
            k=['720p','1080p','480p']
            z=['720p','1080p','480p']
            p=['720p','1080p','480p']
            formats=[]
            for i in fp:
                for j in l:
                    if( j in i):
                         if('x264' in i  and j in k): 
                            formats.append(j+'.x264')
                            link.append(i)
                            k.remove(j)
                         elif('x265' in i and j in z):
                            formats.append(j+'.x265')
                            link.append(i)
                            z.remove(j)
                         elif(j in p):
                            formats.append(j)
                            link.append(i)
                            p.remove(j)
            formats.sort()
            if(formats == []):
                std.addstr(6,1,"sorry, let me try again           ")
                time.sleep(2)
                thread_3=threading.Thread(target=search,args=(s_name.decode("utf-8"),s_seasons.decode("utf-8"),s_episode.decode("utf-8")))
                thread_4=threading.Thread(target=search_tag, args=())
                thread_3.start()
                thread_4.start()
                thread_3.join()
                thread_4.join()
                if(os.stat('epis.txt')):
                    fp= open("epis.txt","r")
                    count=8
                    link=[]
                    l=['720p','1080p','480p']
                    k=['720p','1080p','480p']
                    z=['720p','1080p','480p']
                    p=['720p','1080p','480p']
                    formats=[]
                    for i in fp:
                        for j in l:
                            if( j in i):
                                 if('x264' in i  and j in k): 
                                    formats.append(j+'.x264')
                                    link.append(i)
                                    k.remove(j)
                                 elif('x265' in i and j in z):
                                    formats.append(j+'.x265')
                                    link.append(i)
                                    z.remove(j)
                                 elif(j in p):
                                    formats.append(j)
                                    link.append(i)
                                    p.remove(j)
            formats.sort()
            if(formats  == []):
                std.clear()
                std.addstr(1,1," Sorry try again later please check your input")
                std.addstr(2,1," Suggestion use a proxy server")
                std.getch()
                curses.endwin()
                os.kill(os.getppid(), signal.SIGHUP)
            for i in formats:
                std.addstr(count,1 ,str(formats.index(i)+1)+' '+i)
                count+=1
            std.addstr(count+1,1,"Enter Your choice : ")
            choice =std.getstr(count+1, len("Enter Your choice : "),1)
            value=formats[int(choice.decode("utf-8"))-1]
            find= value.split('.')
            url=''
            flag=1
            fp.close()
            fp = open("epis.txt","r")
            for i in fp:
        ##        std.addstr(count+2,1,i)
                flag=1
                time.sleep(1)
                for j in range(len(find)):
                    if(find[j] in i):
                        pass
                    else:
                        flag=0

                if(flag!=0):
                    url=i
                    break
            std.addstr(count+2,1,url)
            downloader.main(url.strip('\n'))
        ##    std.addstr(11,1,str(link))
            std.refresh()
            std.clear()
            std.refresh()
            std.addstr(1,1,"do you want to add this to you favorite ? 'y' for Yes and 'n' for No ")
            std.addstr(2,1,"* adding this to favorite will automatically download all the latest episode on the arrival on our server")
            std.refresh()
            answer=std.getstr(1,len("do you want to add this to you favorite ? 'y' for Yes and 'n' for No")+2,1)
            if(answer.decode("utf-8")=='y'):
                new=Next_epi.pro()
                std.addstr(4,1,new.New_episode(s_name.decode("utf-8")))
                std.refresh()
            else:
                std.addstr(4,1,"Done, Thankyou!!")        
                std.refresh()
        else:
            std.addstr(4,1,"Sorry!! we searched but couldn't find your episode :( ")
            std.refresh()
        
        std.getch()
        curses.endwin()
    except KeyboardInterrupt:
        std.clear()
        std.addstr(1,1," Thankyou!!")
        std.getch()
        curses.endwin()
        quit()
##        os.kill(os.getppid(), signal.SIGHUP)
##    except :
##        std.clear()
##        std.addstr(1,1," Sorry!! some error has occured please relaunch the application")
##        std.getch()
##        curses.endwin()
##        os.kill(os.getppid(), signal.SIGHUP)                
        
