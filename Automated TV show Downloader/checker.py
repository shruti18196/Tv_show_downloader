#!/usr/bin/python3
import time
import datetime
import os
import User_threads as User_threads_check
import seas_ep_qual_x265_new as seasons_ep_threads_check
import downloader2 as dd

def rewrite(show_name):
    f=open('automate2.txt','r+')
    g=open ('new.txt','w+')
    for line in f:
        if(show_name in line):
            print(line)
            pass
        else:
##         f.seek(f.tell()-len(line))
         g.write(line)
    f.close()
    g.close()
    os.remove('automate2.txt')
    os.rename('new.txt','automate2.txt')
    


def check():
    with open('./automate2.txt') as f:
        for line in f :
            showdetail =line.split(',')
            show_name =showdetail[0].split(' +')[0]
            show_arrival_date = showdetail[0].split('+')[1]+' '+showdetail[1].split(' ')[1]
            arrival_time = showdetail[1].split(' ')[2]
            if( int(arrival_time.split(':')[0]) > 12):
               show_arrival_date += ' 08:00:00'
               show_arrival_date = datetime.datetime.strptime(show_arrival_date,' %B %d %Y %H:%M:%S') + datetime.timedelta(days=1)
            else:
               show_arrival_date = datetime.datetime.strptime(show_arrival_date,' %B %d %Y')
               show_arrival_date = show_arrival_date.replace(hour=21,minute=0)
               print(show_arrival_date)
            season = showdetail[2].split(':')[1]
            episode = showdetail[3].split(':')[1].strip('\n')
            dat=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
##            print(type(datetime.datetime.strptime(dat,"%Y-%m-%d %H:%M:%S")),dat,type(show_arrival_date),show_arrival_date)
            if(show_arrival_date <= datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")):
                 User_threads_check.final(show_name)
                 seasons_ep_threads_check.final(season,episode)
                 f= open('epis.txt','r+')
                 for i in f:
                         if '720' in i:
                             dd.main(i.strip('\n'))
                             
                 rewrite(show_name)
                 return True         
            else:
                 return False

