#!/usr/bin/python3
import urllib.request as ur
import requests
import time
import threading
import curses

global stdscr

class download:
    def __init__(self):
    
        self.url = 'http://www.top4themes.com/data/out/134/6545537-superman-logo-wallpapers.jpg'
        self.req= ur.urlopen(self.url)
        self.count = 0
        self.block_size = 1024
        avg=0
        smin = []
        value = False
        t=[]
        while True:
            stdscr.refresh()
            start = time.time()
            buff = self.    req.read(self.block_size)
            stop = time.time()
            avg += len(buff)
            if not buff:
               break;
            if (stop-start)< 0.2 : 
                self.block_size += 2048
            elif (stop-start) > 0.2:
                self.block_size -= 1024
            self.count+=1
##            stdscr.addstr(0,0,"blocksize {}".format(self.block_size))
            t.append(int(self.block_size))
        if(self.block_size ==0):
            self.block_size=max(t)
##        stdscr.addstr(dim[0],dim[1]-count-1, h)
##        stdscr.addstr(0,0,"blocksize {}".format(self.block_size))
##        self.downloader()
            
    def requa(self,byte):

        header = {'Range':"bytes=%s- "%str(byte),'Connection':'close','USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        try:
            requ = requests.get(self.url, headers=header, stream=True)
##            print(requ.status_code)
            if(requ.status_code==206):
                    return requ
            else:
                    return None
        except Exception as e :
            pass
##           print(str(e)+'\n')

    def write_2(self,requ,file_size,ini,threadLock,f,no):
        download_status = 0
        download = 0
        avg = 0
        count = 0
        start =time.time()
        count=0
        pos=ini
        time_1=0
##        print(pos)
        try :
            for buff in requ.iter_content(chunk_size=self.block_size):
##                while self.value!=False:
##                    print("Thread {}  paused".format(no))
##                    time.sleep(1)
##                    time_1+=1
##                    if(time_1 ==3):
##                        self.value=False
                threadLock.acquire()
##                stdscr.clrtoeol()
                time_spend=time.time() - start
                download += len(buff)
                count+=1
                f.seek(pos)
                download_status = (download*100.00/int(file_size-ini))
                if( time_spend == 0):
                     time_spend=1   
                speed = download/(1024*time_spend)
                if(ini+count*self.block_size>= file_size):
                    f.write(buff[0:file_size-count*self.block_size-ini])
                    f.flush()
                    threadLock.release()
##                    stdscr.clrtoeol()
                    break
                else:
                    f.write(buff)
                    f.flush()
                    pos+=len(buff)
                    if(download_status> 50 and time_1!=3):
                         self.value= True
##                stdscr.clrtoeol()
##                stdscr.addstr(5+no,0,"Thread {} : {}% {}KB/s  {}MB seconds : {} ".format(no,round(download_status,2),speed,round(download/1024/1024,2),round(time_spend,3)))
##                stdscr.refresh()
                threadLock.release()
        except Exception as e:
            pass
##             stdscr.addstr(5+no,0,str(e))
             
##        stdscr.clrtoeol()
##        stdscr.addstr(5+no,0,"thread {} completed ".format(no))
##        stdscr.refresh()

        
    def write_3(self,requ,file_size,ini,threadLock,f):
        download_status = 0
        download = 0
        avg = 0
        count = 0
        start =time.time()
        count=0
        pos = ini
##        print(pos)
        try:
            for buff in requ.iter_content(chunk_size=self.block_size):
                threadLock.acquire()
                time_spend=time.time() - start
                download += len(buff)
                f.seek(pos)
                f.write(buff)
                count+=1
                download_status = (download*100.00/int(file_size-ini))
                if( time_spend ==0):
                     time_spend=1   
                speed = download/(1024*time_spend)
                f.flush()
                pos+= len (buff)
##                stdscr.addstr(10,0,"Thread 3 : {}% {}KB/s completed {}MB seconds passed {} ".format(download_status,speed,download/1024/1024,time_spend))
                threadLock.release()
        except Exception as e:
            print(str(e))
##        stdscr.addstr(10,0,"thread 3 completed ")

        
    def downloader(self,url1):


            self.url = url1
            header = { 'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0','Connection':'close'}
            try:
                req= requests.get(self.url,stream=True)
            except requests.exceptions.RequestException as e:
                stdscr.addstr(14,0,(str(e)))
            file_name=self.url.split('/')[-1]
            f = open(file_name,'wb+')
            f.close()
            f = open(file_name,'rb+')
            stdscr.refresh()
            file_size = (req.headers['Content-Length'])    #req.headers returns a dictionary
##            stdscr.addstr(1,0, "Downloading : {} Mega Bytes: {} ".format(file_name,round(int(file_size)/1024/1024,2)))
##            stdscr.refresh()
####            stdscr.addstr(2,0,str(req.headers))
##            stdscr.refresh()
            if (req.headers['Accept-Ranges'] !='bytes'):
##                print(' Non-resumable content ')
                file_size=int(file_size)
##                print(self.block_size)
                download_status = 0
                download = 0
                avg = 0
                count = 0
                speed = 0
                threadLock = threading.Lock()
                start =time.time()
                self.write_3(req3,file_size,0,threadLock,f)
                
            else:
##                stdscr.addstr(2,0,'Resumable content {}'.format(req.headers['Connection']))
##                stdscr.refresh()
                file_size=int(file_size)
                stdscr.addstr(3,0,"{}".format(self.block_size))
                stdscr.refresh()
                download_status = 0
                download = 0
                avg = 0
                count = 0
                speed = 0
                threadLock = threading.Lock()
                req_1 =[req]
                series = [4/8,6/8,2/8,3/8,5/8,1/8,7/8]
##                series= [8/16,4/16,12/16,6/16,10/16,7/16,11/16,5/16,9/16,2/16,14/16,3/16,13/16,1/16,15/16] 
                valid =[0]
            
                for i  in series:
                    req_temp = self.requa(int(i*file_size))
                    if(req_temp!=None):
                        req_1.append(req_temp)
                        valid.append(i)
                    else:
                        pass
                valid.append(1)
##                print(valid)
                valid.sort()
                series=[0]+series
##                print(series)
                count=[]
                for i in series:
                    if(i in valid):
                        count.append(int(valid[valid.index(i)+1]*file_size))
                    else:
                        pass
                thread=[]
##                print (count)
##                self.block_size=1024
                for i,c,v in zip(req_1,count,series):
                    t =threading.Thread(target=self.write_2, args=(i,c,int(v*file_size),threadLock,f,req_1.index(i)+1))
                    thread.append(t)
##                    print (" {} {} {} {}".format(i,c/file_size,v,req_1.index(i)))
##                stdscr.addstr(4,0,"No. of threads {}".format(len(thread)))
##                stdscr.refresh()
##                time.sleep(10)
                start = time.time()
                for i in thread:
                    i.start()
                for i in thread:
                    i.join()
 
            f.close()
            time_spend =time.time()-start
##            stdscr.clrtoeol()
##            stdscr.addstr(14,0,"total time {} ".format(time_spend))
##            stdscr.refresh()


def main(url1):
##    global stdscr
##    stdscr = curses.initscr()
##    stdscr.clear()
##    curses.noecho()
##    curses.cbreak()
    a= download()
    a.downloader(url1)
##    stdscr.addstr(20,0,url1)
##    time.sleep(5)
##    curses.echo()
##    curses.nocbreak()
##    curses.endwin()

    


   
    
