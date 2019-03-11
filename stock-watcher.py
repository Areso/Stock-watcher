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

    myassets = shares[0].split(";")
    myexchanges = shares[1].split(";")
    mythreshold_low = shares[2].split(";")
    mythreshold_high = shares[3].split(";")
    myassets = myassets[:-1]
    myexchanges = myexchanges[:-1]
    mythreshold_low = mythreshold_low[:-1]
    mythreshold_high = mythreshold_high[:-1]

    amountofassets = len(myassets)

    sms_counter_dict = {}

    if len(myassets) > 0:
        for each_asset in myassets:
            sms_counter_dict[each_asset] = 0

    global sms_counter, threshold_min, threshold_max
    sms_counter = 0
    threshold_min = 270
    threshold_max = 300
    myparams = []
    myparams.append(mykey)
    myparams.append(mynumber)
    # myparams.append(sms_counter)
    # myparams.append(threshold_min)
    # myparams.append(threshold_max)
    return myparams, myassets, myexchanges, mythreshold_low, mythreshold_high, sms_counter_dict


def test():
    return 2,3,4


def parsing_spbexchange(parsing_params):
    url = "http://spbexchange.ru/ru/market-data/Default.aspx"
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(response.text, "html.parser")
    mytext = soup.get_text()
    mypos = mytext.find(parsing_params)
    size_of_line = 120
    my_listing_text = (mytext[mypos:mypos + size_of_line])
    my_listing_values = my_listing_text.split()
    my_listing_price = []

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


def main_loop(loop_params, loop_assets, loop_exchanges, loop_threshold_low, loop_threshold_high, loop_sms_counter_dict):
    while True:
        myiterator = 0
        for each_asset in loop_assets:
            price = parsing_spbexchange(each_asset)
            threshold_low = float(loop_threshold_low[myiterator])
            threshold_max = float(loop_threshold_high[myiterator])
            print(price)
            if price != 0:
                print('low threshold is '+str(threshold_low))
                print('max threshold is ' + str(threshold_max))
                # TODO send asset's name, threshold passed, threshold value
                if price < threshold_low and sms_counter == 0:
                    send_message('min threshold is passed', loop_params)
                if price > threshold_max and sms_counter == 0:
                    send_message('max threshold is passed', loop_params)
            myiterator = myiterator + 1
        time.sleep(5)


if __name__ == "__main__":
    myparams, myassets, myexchanges, mythreshold_low, mythreshold_high, sms_counter_dict = myloading()
    main_loop(myparams, myassets, myexchanges, mythreshold_low, mythreshold_high, sms_counter_dict)
else:
    print("the program is being imported into another module")
