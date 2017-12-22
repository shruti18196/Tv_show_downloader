#!/usr/bin/python3
import urllib.request

def internet_on():
    try:
        response=urllib.request.urlopen('http://www.google.com',timeout=20)
        return 'True'
    except : pass
    return 'False'

##print(internet_on())


