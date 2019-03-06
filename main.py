#!/usr/bin/python
import sys
import urllib3
from time import sleep
from bs4 import BeautifulSoup
import requests
url = "http://spbexchange.ru/ru/market-data/Default.aspx"

response = requests.get(url)
page = response.text

soup = BeautifulSoup(response.text, "html.parser")
mytext = soup.get_text()
mypos = mytext.find("TSLA")
sizeOfLine = 120
myTSLAtext = (mytext[mypos:mypos+sizeOfLine])
myTSLAlist = myTSLAtext.split()
myTSLAlistClear = []
print(len(myTSLAlist))
# print(myTSLAtext.count('\n'))

i = 0
for myelement in myTSLAlist:
    if i < 15:
        if i == 9:
            myTSLAlistClear.append(myelement)
    i = i + 1

# myTSLAlistClear.append('279,84')  # debug message

print(myTSLAlistClear)
threshold_min = 270
threshold_max = 300

if len(myTSLAlistClear) > 0:
    price = (myTSLAlistClear[0])
    price = price.replace(",", ".")
    price = float(price)
    if price < threshold_min:
        print('send SMS threshold min')
    if price > threshold_max:
        print('send SMS threshold max')

#https://sms.ru/sms/send?api_id=key&to=phonenumber&msg=hello+world&json=1