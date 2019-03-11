#!/usr/bin/python3
import sys
import os
import urllib3
from time import sleep
from bs4 import BeautifulSoup
import requests
import time
import traceback


def send_message(mymessage, message_params):
    sms_url = 'https://sms.ru/sms/send?api_id=key&to=number&msg=message&json=1'
    sms_url = sms_url.replace('key', mykey)
    sms_url = sms_url.replace('number', mynumber)
    sms_url = sms_url.replace('message', mymessage)
    sms_response = requests.get(sms_url)
    print('sms sent') # debug
    global sms_counter
    sms_counter = sms_counter + 1


def myloading():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keypath = dir_path + '\\'
    mynumberpath = dir_path + '\\'

    f = open(keypath + "key.txt", "r")
    global mykey
    mykey = f.read()
    # mykey = 'key' # debug
    f.close()

    f = open(mynumberpath + "config.txt", "r")
    global mynumber
    mynumber = f.read()
    # mynumber = '922' # debug
    f.close()

    global myshares
    shares = []
    # f = open(keypath + "shares.txt", "r")
    with open(keypath + "shares.txt") as f:
        for line in f:
            shares.append(line)

    #myshares = f.read()
    # mykey = 'key' # debug
    #print(myshares)
    #print(type(myshares))
    #print(len(shares))
    #f.close()



    global sms_counter, threshold_min, threshold_max
    sms_counter = 0
    threshold_min = 270
    threshold_max = 300
    myparams = []
    myparams.append(mykey)
    myparams.append(mynumber)
    myparams.append(sms_counter)
    myparams.append(threshold_min)
    myparams.append(threshold_max)
    return myparams


def parsing_spbexchange(parsing_params):
    url = "http://spbexchange.ru/ru/market-data/Default.aspx"
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(response.text, "html.parser")
    mytext = soup.get_text()
    mypos = mytext.find("TSLA")
    sizeOfLine = 120
    my_listing_text = (mytext[mypos:mypos + sizeOfLine])
    my_listing_values = my_listing_text.split()
    my_listing_price = []
    # print(myTSLAtext.count('\n'))

    i = 0
    for myelement in my_listing_values:
        if i < 15:
            if i == 9:
                my_listing_price.append(myelement)
        i = i + 1

    # my_listing_price.append('279,84')  # debug message

    if len(my_listing_price) > 0:
        price = (my_listing_price[0])
        price = price.replace(",", ".")
        price = float(price)
        return price
    else:
        price = 0
        return price


def main_cicle(cicle_params):
    while True:
        price = parsing_spbexchange(cicle_params)
        print(price)
        if price != 0:
            if price < threshold_min and sms_counter == 0:
                send_message('min threshold is passed', cicle_params)
            if price > threshold_max and sms_counter == 0:
                send_message('max threshold is passed', cicle_params)
        time.sleep(5)


if __name__ == "__main__":
    myparams = myloading()
    main_cicle(myparams)
else:
    print("the program is being imported into another module")
