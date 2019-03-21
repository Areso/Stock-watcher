#!/usr/bin/python3
# This script licensed under AGPLv3 License
# This very version made by Anton Gladyshev (Areso)
import sys
import os
from bs4 import BeautifulSoup
import requests
import time
# from selenium import webdriver
from requests_html import HTMLSession


def send_message(mymessage, msg_params, msg_asset, msg_threshold, msg_price, msg_sms_counter_dict):
    sms_url = 'https://sms.ru/sms/send?api_id=key&to=number&msg=message&json=1'
    sms_url = sms_url.replace('key', msg_params[0])
    sms_url = sms_url.replace('number', msg_params[1])
    message = ''
    if mymessage == 'min':
        message = 'Asset '+msg_asset+' is passed MIN threshold ('+str(msg_threshold)\
                  + ') with current asset price ' + str(msg_price)
    elif mymessage == 'max':
        message = 'Asset ' + msg_asset + ' is passed MAX threshold (' + str(msg_threshold)\
                  + ') with current asset price ' + str(msg_price)
    print(message)
    sms_url = sms_url.replace('message', message)
    # TODO try block. Sometimes SMS.RU get stuck
    sms_response = requests.get(sms_url)
    print('sms sent')
    msg_sms_counter_dict[msg_asset] = msg_sms_counter_dict[msg_asset] + 1
    return msg_sms_counter_dict


def myloading():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keypath = dir_path + '\\'
    mynumberpath = dir_path + '\\'

    f = open(keypath + "key.txt", "r")
    mykey = f.read()
    f.close()

    f = open(mynumberpath + "config.txt", "r")
    mynumber = f.read()
    f.close()

    shares = []
    with open(keypath + "shares.txt") as f:
        for line in f:
            shares.append(line)

    myassets = shares[0].split(";")
    myexchanges = shares[1].split(";")
    mythreshold_min = shares[2].split(";")
    mythreshold_max = shares[3].split(";")
    myassets = myassets[:-1]
    myexchanges = myexchanges[:-1]
    mythreshold_min = mythreshold_min[:-1]
    mythreshold_max = mythreshold_max[:-1]

    sms_counter_dict = {}

    if len(myassets) > 0:
        for each_asset in myassets:
            sms_counter_dict[each_asset] = 0

    myparams = []
    myparams.append(mykey)
    myparams.append(mynumber)
    return myparams, myassets, myexchanges, mythreshold_min, mythreshold_max, sms_counter_dict


def parsing_spbexchange(parsing_asset):
    url = "http://spbexchange.ru/ru/market-data/Default.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mytext = soup.get_text()
    mypos = mytext.find(parsing_asset)
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


def parsing_tradingview(parsing_asset, parsing_exchange):
    url = "https://www.tradingview.com/symbols/"
    url = url + parsing_exchange + '-' + parsing_asset
    print(url)
    #response = requests.get(url)
    #page = response.text
    #print(page)

    session = HTMLSession()
    r = session.get(url)
    my = r.html.render(timeout=30)
    test = r.html.search('js-symbol-last')

    #soup = BeautifulSoup(my, "html.parser")
    #price = soup.find_all(class_='js-symbol-last')
    #price = soup.prettify()
    #price = soup.select(selector)
    #price = soup.find('tv-symbol-header-quote__value tv-symbol-header-quote__value--large js-symbol-last')

    selector = 'span.tv-symbol-header-quote__value.tv-symbol-header-quote__value--large.js-symbol-last'
    price = r.html.find(selector)[0].text
    r.close()
    session.close()
    try:
        price = float(price)
    except:
        price = 0
    finally:
        return price


def parsing_tinkoff(parsing_asset):
    url = "https://www.tinkoff.ru/invest/stocks/"
    url = url + parsing_asset
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    inputTag = soup.findAll(attrs={"data-qa-file": "Money"})
    priceline = inputTag[0]
    priceline = priceline.get_text()
    priceline = priceline[:-2]
    priceline = priceline.replace(",", ".")
    try:
        price = float(priceline)
    except:
        price = 0
    finally:
        return price


def main_loop(loop_params, loop_assets, loop_exchanges, loop_threshold_min, loop_threshold_max, loop_sms_counter_dict):
    while True:
        myiterator = 0
        for each_asset in loop_assets:
            # price = parsing_spbexchange(each_asset)
            # price = parsing_tradingview(each_asset, loop_exchanges[myiterator])
            price = parsing_tinkoff(each_asset)
            threshold_min = float(loop_threshold_min[myiterator])
            threshold_max = float(loop_threshold_max[myiterator])
            sms_counter = loop_sms_counter_dict[each_asset]
            print(price)
            if price != 0:
                # print('min threshold is ' + str(threshold_min)) # debug
                # print('max threshold is ' + str(threshold_max)) # debug
                # print(str(sms_counter)) # debug
                if price < threshold_min and sms_counter == 0:
                    loop_sms_counter_dict = send_message('min', loop_params, each_asset, threshold_min, price, loop_sms_counter_dict)
                if price > threshold_max and sms_counter == 0:
                    loop_sms_counter_dict = send_message('max', loop_params, each_asset, threshold_max, price, loop_sms_counter_dict)
            myiterator = myiterator + 1
        time.sleep(15)


if __name__ == "__main__":
    ld_params, ld_assets, ld_exchanges, ld_threshold_min, ld_threshold_max, ld_sms_counter_dict = myloading()
    main_loop(ld_params, ld_assets, ld_exchanges, ld_threshold_min, ld_threshold_max, ld_sms_counter_dict)
else:
    print("the program is being imported into another module")
