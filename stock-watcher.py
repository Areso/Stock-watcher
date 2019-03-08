#!/usr/bin/python3
import sys
import os
import urllib3
from time import sleep
from bs4 import BeautifulSoup
import requests
import time
import traceback


def send_message(mymessage):
    sms_url = 'https://sms.ru/sms/send?api_id=key&to=number&msg=message&json=1'
    sms_url = sms_url.replace('key', mykey)
    sms_url = sms_url.replace('number', mynumber)
    sms_url = sms_url.replace('message', mymessage)
    print(sms_url)
    #sms_response = requests.get(sms_url)
    global sms_counter
    sms_counter = sms_counter + 1


INDENT = '   '
mycallstack = traceback.format_stack()
mycallstack = mycallstack[0]
mypos = mycallstack.find('\"')
deletepart = mycallstack[0:mypos+1]
mycallstack = mycallstack.replace(deletepart, '')
mypos = mycallstack.find('\"')
deletepart = mycallstack[0:mypos+1]
mypos = mycallstack.find('\"')
mycallstack = mycallstack[0:mypos]


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

keypath = dir_path+'\\'
mynumberpath = dir_path+'\\'

f = open(keypath+"key.txt", "r")
mykey = f.read()
# mykey = 'key' # debug
f.close()

f = open(mynumberpath+"config.txt", "r")
mynumber = f.read()
# mynumber = '922' # debug
f.close()

sms_counter = 0
threshold_min = 270
threshold_max = 300
url = "http://spbexchange.ru/ru/market-data/Default.aspx"



while True:
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(response.text, "html.parser")
    mytext = soup.get_text()
    mypos = mytext.find("TSLA")
    sizeOfLine = 120
    myTSLAtext = (mytext[mypos:mypos+sizeOfLine])
    myTSLAlist = myTSLAtext.split()
    myTSLAlistClear = []
    # print(myTSLAtext.count('\n'))

    i = 0
    for myelement in myTSLAlist:
        if i < 15:
            if i == 9:
                myTSLAlistClear.append(myelement)
        i = i + 1

    # myTSLAlistClear.append('279,84')  # debug message

    if len(myTSLAlistClear) > 0:
        price = (myTSLAlistClear[0])
        price = price.replace(",", ".")
        price = float(price)
        print(price)
        if price < threshold_min and sms_counter == 0:
            send_message('min threshold is passed')
        if price > threshold_max and sms_counter == 0:
            send_message('max threshold is passed')
    time.sleep(5)
