
import time
import datetime
from datetime import date
from datetime import datetime
import calendar
import xlrd
import xlwt
from xlwt import Workbook
import csv
from itertools import islice
import re
import os, os.path
import math
import matplotlib.pyplot as plt
import requests
import tosdb
import urllib
from splinter import Browser
import multiprocessing
from multiprocessing import Process, Manager, Lock
starttime = time.time()
import numpy as np







path = 'C:/Users/shiva/PycharmProjects/BotTest/'
files = os.listdir(path)
file_list =([])
for n in range(0,len(files)):
    if files[n].endswith('.csv'):
        # file_list = np.append(file_list,files[n])
        file_list.append(files[n])


threads = 10
num_files = len(file_list) - 1
# num_files = 80

def findstraight(x):
    straightness = 0
    for n in range(0, len(x) - 1):
        q = math.sqrt((-1) ** 2 + (x[n] - x[n + 1]) ** 2)
        straightness = straightness + q
    p = math.sqrt((len(x)**2) + (x[-1]**2))
    straight = p/straightness
    return straight

def strat1(z, L,d, lock):
    buy_in = ([0] * 24)
    PL = 0
    Bal = 0
    Hourly_PL = ([0] * 7)

    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 30
    mark_up = [0] * 30
    stop_loss = [0] * 30
    Entry_Price = [0] * 30
    Recent_Exit = [1] * 30
    hourly = [0] * 24
    totdiff = 0
    avgpercent = 0
    low = [10000] * 20
    high = [0] * 20
    times_entered = [0] * 30



    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/'  + str(file_list[z])

    times_entered = [0] * 30
    Recent_Exit = [1] * 30

    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Time_data = []

    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0,22):
                    row[ii] = float(row[ii])

                Entry = row[:20]
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time)-1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue


            if (Entry[2] < 0):
                Recent_Exit[count] = 0
            if (Entry[17] > 65) and (Entry[18] > 65) and (Entry[19] > 65) and (Entry[3] > 0) and (Entry[6] > 0) and (Recent_Exit[count] == 0) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = 9 // Entry[9]
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                # Bal = Bal - (numshare * price) * 1.000120555
                # Bal = Bal - (numshare * Entry[15])

                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1

                stop_loss[count] = price - (Entry[9] * 2)
                mark_up[count] = price + (Entry[9] * 1)

            if Pos[count] > 0:
                if (price < stop_loss[count]) and (times_entered[count] < 12):
                    stop_loss[count] = stop_loss[count] - (Entry[9])
                    numshare = Pos[count] // 7
                    Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                    Bal = Bal - (numshare * price)
                    Pos[count] = Pos[count] + numshare
                    times_entered[count] = times_entered[count] + 1
                    Ins = Ins + 1
                if (price > mark_up[count]) or (hour == 14 and min == 59):
                    returnval = Pos[count] * price
                    # returnval = Pos[count]*price *(1 - 0.000120555)
                    # returnval = Pos[count]*Entry[16]

                    Bal = Bal + returnval
                    diff = price - Entry_Price[count]
                    diff = diff / Entry_Price[count]
                    totdiff = totdiff + diff
                    avgpercent = 100 * totdiff / Ins
                    if price > Entry_Price[count]:
                        win = win + 1
                        wintot = wintot + (Pos[count] * price - Pos[count] * Entry_Price[count]) / (Entry_Price[count])
                        winav = wintot / win
                    else:
                        lose = lose + 1
                        losstot = losstot + (Pos[count] * Entry_Price[count] - Pos[count] * price) / (Entry_Price[count])
                        lossav = losstot / lose
                    Entry_Price[count] = 0
                    Pos[count] = 0
                    Recent_Exit[count] = 1
                    buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL =  Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z*7):(z*7+7)] =  Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] *  d['wins']) + (win * winav))/(d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] *  d['losses']) + (lose * lossav))/(d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] *  d['Entries'])/100) + totdiff)/(d['Entries'] + Ins))* 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat2(z, L,d, lock):
    buy_in = [0] * 24
    PL = 0
    Bal = 0
    Hourly_PL = [0] * 7

    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 30
    mark_up = [0] * 30
    stop_loss = [0] * 30
    Entry_Price = [0] * 30
    Recent_Exit = [1] * 30
    hourly = [0] * 24
    totdiff = 0
    avgpercent = 0
    low = [10000] * 30
    high = [0] * 20
    times_entered = [0] * 30



    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/'  + str(file_list[z])

    times_entered = [0] * 30
    Recent_Exit = [1] * 30

    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Time_data = []

    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0,22):
                    row[ii] = float(row[ii])

                Entry = row[:20]
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time)-1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue


            if (Entry[2] < 0):
                Recent_Exit[count] = 0
            if (Entry[17] > 65) and (Entry[18] > 65) and (Entry[19] > 65) and (Entry[3] > 0) and (Entry[6] > 0) and (Recent_Exit[count] == 0) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = (40 // Entry[9]) * (8/(hour * 2))
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)


                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1

                stop_loss[count] = price - (Entry[9] * 4)
                mark_up[count] = price + (Entry[9] * 2)

            if Pos[count] > 0:
                # if (price < stop_loss[count]) and (times_entered[count] < 6):
                #     stop_loss[count] = stop_loss[count] - (Entry[9])
                #     numshare = Pos[count] // 7
                #     Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                #     Bal = Bal - (numshare * price)
                #     Pos[count] = Pos[count] + numshare
                #     PerStock[count][1] = PerStock[count][1] - (numshare * price)
                #     PerStock[count][2][len(PerStock[count][2]) - 1] = PerStock[count][2][len(
                #         PerStock[count][2]) - 1] + str(hour % 12) + ':' + str("{:02d}".format(min)) + '(' + str(
                #         price) + ')'
                #     times_entered[count] = times_entered[count] + 1
                #     Ins = Ins + 1
                if (price > mark_up[count]) or (hour == 14 and min == 59):
                    returnval = Pos[count] * price
                    # returnval = Pos[count]*price *(1 - 0.000120555)
                    # returnval = Pos[count]*Entry[16]

                    Bal = Bal + returnval
                    diff = price - Entry_Price[count]
                    diff = diff / Entry_Price[count]
                    totdiff = totdiff + diff
                    avgpercent = 100 * totdiff / Ins
                    if price > Entry_Price[count]:
                        win = win + 1
                        wintot = wintot + (Pos[count] * price - Pos[count] * Entry_Price[count]) / (Entry_Price[count])
                        winav = wintot / win
                    else:
                        lose = lose + 1
                        losstot = losstot + (Pos[count] * Entry_Price[count] - Pos[count] * price) / (Entry_Price[count])
                        lossav = losstot / lose
                    Entry_Price[count] = 0
                    Pos[count] = 0
                    Recent_Exit[count] = 1
                    buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL =  Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z*7):(z*7+7)] =  Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] *  d['wins']) + (win * winav))/(d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] *  d['losses']) + (lose * lossav))/(d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] *  d['Entries'])/100) + totdiff)/(d['Entries'] + Ins))* 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat3(z, L,d, lock):
    buy_in = [0] * 24
    PL = 0
    Bal = 0
    Hourly_PL = [0] * 7
    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 30
    mark_up = [0] * 30
    stop_loss = [0] * 30
    Entry_Price = [0] * 30
    Recent_Exit = [1] * 30
    hourly = [0] * 24
    totdiff = 0
    winwin = 0
    avgpercent = 0
    low = [10000] * 30
    high = [0] * 30
    times_entered = [0] * 30
    markdown = [0] * 30


    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/'  + str(file_list[z])

    times_entered = [0] * 30
    Recent_Exit = [1] * 30

    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Time_data = []

    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0,22):
                    row[ii] = float(row[ii])

                Entry = row[:20]
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time)-1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue

            if (Entry[2] < 0):
                Recent_Exit[count] = 0
            if (Entry[17] > Entry[18]) and (Entry[18] > Entry[19]) and (Entry[17] > 60) and (Entry[3] > 0) and (Entry[6] > 0) and (Recent_Exit[count] == 0) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = 2.5 // Entry[9]
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1

                stop_loss[count] = price - (Entry[9] * 1)
                mark_up[count] = price + (Entry[9] * 3)
                markdown[count] = price - (Entry[9] * .1)

            if Pos[count] > 0:
                if (price < markdown[count]):
                    markdown[count] = markdown[count] - (Entry[9]) * .1
                    numshare = Pos[count] // 3
                    Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                    Bal = Bal - (numshare * price)
                    Pos[count] = Pos[count] + numshare
                    times_entered[count] = times_entered[count] + 1
                    Ins = Ins + 1
                if (price > mark_up[count]) or (price < stop_loss[count]) or (hour == 14 and min == 59):
                    returnval = Pos[count] * price
                    # returnval = Pos[count]*price *(1 - 0.000120555)
                    # returnval = Pos[count]*Entry[16]

                    Bal = Bal + returnval
                    diff = price - Entry_Price[count]
                    diff = diff / Entry_Price[count]
                    totdiff = totdiff + diff
                    avgpercent = 100 * totdiff / Ins
                    if price > Entry_Price[count]:
                        win = win + 1
                        wintot = wintot + (Pos[count] * price - Pos[count] * Entry_Price[count]) / (Entry_Price[count])
                        winav = wintot / win
                    else:
                        lose = lose + 1
                        losstot = losstot + (Pos[count] * Entry_Price[count] - Pos[count] * price) / (Entry_Price[count])
                        lossav = losstot / lose
                    Entry_Price[count] = 0
                    Pos[count] = 0
                    Recent_Exit[count] = 1
                    buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL =  Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z*7):(z*7+7)] =  Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] *  d['wins']) + (win * winav))/(d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] *  d['losses']) + (lose * lossav))/(d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] *  d['Entries'])/100) + totdiff)/(d['Entries'] + Ins))* 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat4(z, L,d, lock):
    buy_in = [0] * 24
    PL = 0
    Bal = 0
    Hourly_PL = [0] * 7
    PerStock = [[[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]]]
    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 30
    mark_up = [0] * 30
    stop_loss = [0] * 30
    Entry_Price = [0] * 30
    Recent_Exit = [1] * 30
    hourly = [0] * 24
    totdiff = 0
    avgpercent = 0
    low = [10000] * 30
    high = [0] * 30
    times_entered = [0] * 30



    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/'  + str(file_list[z])

    times_entered = [0] * 30
    Recent_Exit = [1] * 30

    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Time_data = []

    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0,22):
                    row[ii] = float(row[ii])

                Entry = row[:20]
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time)-1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
            else:
                count = 0
                stockval = 0
                continue


            if (Entry[2] < 0):
                Recent_Exit[count] = 0
            if (Entry[0] > 0) and (Entry[10] > 0) and (Entry[11] < 0) and (Entry[1] > 0) and (Entry[2] > 0) and (Entry[19] < 65) and (Entry[3] > 0) and (Entry[4] > 0) and (Entry[6] > 0) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = 7 // Entry[9]
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                # Bal = Bal - (numshare * price) * 1.000120555
                # Bal = Bal - (numshare * Entry[15])

                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1
                times_entered[count] = 1

                stop_loss[count] = price - (Entry[9] * 1)
                mark_up[count] = price + (Entry[9] * 4)

            if Pos[count] > 0:
                if (price < stop_loss[count]) and (times_entered[count] < 12):
                    stop_loss[count] = stop_loss[count] - (Entry[9])
                    numshare = Pos[count] // 10
                    Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                    Bal = Bal - (numshare * price)
                    Pos[count] = Pos[count] + numshare

                    times_entered[count] = times_entered[count] + 1
                    Ins = Ins + 1
                if (Entry[11] > 0):
                    buy_in[count] = 1
                if ((price > mark_up[count]) and (times_entered[count] > 1)) or ((Entry[11] < 0) and (price > Entry_Price[count]) and (buy_in[count] == 1) and (times_entered[count] == 1)) or (times_entered[count] >= 12) or (hour == 14 and min == 59):
                    returnval = Pos[count] * price
                    # returnval = Pos[count]*price *(1 - 0.000120555)
                    # returnval = Pos[count]*Entry[16]

                    Bal = Bal + returnval

                    diff = price - Entry_Price[count]
                    diff = diff / Entry_Price[count]
                    totdiff = totdiff + diff
                    avgpercent = 100 * totdiff / Ins
                    if price > Entry_Price[count]:
                        win = win + 1
                        wintot = wintot + (Pos[count] * price - Pos[count] * Entry_Price[count]) / (Entry_Price[count])
                        winav = wintot / win
                    else:
                        lose = lose + 1
                        losstot = losstot + (Pos[count] * Entry_Price[count] - Pos[count] * price) / (Entry_Price[count])
                        lossav = losstot / lose
                    Entry_Price[count] = 0
                    Pos[count] = 0
                    Recent_Exit[count] = 1
                    buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if stockval > maxspend:
                maxspend = int(stockval)
            PL =  Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z*7):(z*7+7)] =  Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] *  d['wins']) + (win * winav))/(d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] *  d['losses']) + (lose * lossav))/(d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] *  d['Entries'])/100) + totdiff)/(d['Entries'] + Ins))* 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat5(z, L,d, lock):
    buy_in = [0] * 30
    PL = 0
    Bal = 0
    Hourly_PL = [0] * 7

    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 30
    mark_up = [0] * 30
    stop_loss = [0] * 30
    Entry_Price = [0] * 30
    Recent_Exit = [1] * 30
    hourly = [0] * 30
    totdiff = 0
    avgpercent = 0
    low = [10000] * 30
    high = [0] * 30
    times_entered = [0] * 30
    shareconst = .7


    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/'  + str(file_list[z])

    times_entered = [0] * 30
    Recent_Exit = [1] * 30

    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Time_data = []

    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0,22):
                    row[ii] = float(row[ii])

                Entry = row[:20]
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time)-1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue


            if (Entry[2] < 0):
                Recent_Exit[count] = 0
            # if (Entry[5] > 0) and (price > Entry[8]) and (Entry[12] < 0) and (Entry[13] > 0) and (Entry[2] > 0) and (Entry[4] > 0) and (Entry[6] > 0) and (Recent_Exit[count] == 0) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
            if  (Entry[2] > 0) and (Entry[3] > 0) and (Entry[4] > 0) and (Entry[5] > 0) and (Entry[6] > 0) and (Entry[8] < price) and (Entry[12] < 0) and (Entry[13] > 0)  and (Recent_Exit[count] == 0) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = math.ceil((40 // Entry[9])* shareconst)
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                # Bal = Bal - (numshare * price) * 1.000120555
                # Bal = Bal - (numshare * Entry[15])

                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1

                stop_loss[count] = price - (Entry[9] * 2)
                mark_up[count] = price + (Entry[9] * 2)
                times_entered[count] = 0

            if Pos[count] > 0:
                if (price < stop_loss[count]) and (times_entered[count] < 12):
                    stop_loss[count] = stop_loss[count] - (Entry[9])
                    numshare = math.ceil((Pos[count] // 7) * shareconst)
                    Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                    Bal = Bal - (numshare * price)
                    Pos[count] = Pos[count] + numshare

                    times_entered[count] = times_entered[count] + 1
                    Ins = Ins + 1
                if (price > mark_up[count]) or (hour == 14 and min == 59):
                    returnval = Pos[count] * price
                    # returnval = Pos[count]*price *(1 - 0.000120555)
                    # returnval = Pos[count]*Entry[16]

                    Bal = Bal + returnval

                    diff = price - Entry_Price[count]
                    diff = diff / Entry_Price[count]
                    totdiff = totdiff + diff
                    avgpercent = 100 * totdiff / Ins
                    if price > Entry_Price[count]:
                        win = win + 1
                        wintot = wintot + (Pos[count] * price - Pos[count] * Entry_Price[count]) / (Entry_Price[count])
                        winav = wintot / win
                    else:
                        lose = lose + 1
                        losstot = losstot + (Pos[count] * Entry_Price[count] - Pos[count] * price) / (Entry_Price[count])
                        lossav = losstot / lose
                    Entry_Price[count] = 0
                    Pos[count] = 0
                    Recent_Exit[count] = 1
                    buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL =  Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z*7):(z*7+7)] =  Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] *  d['wins']) + (win * winav))/(d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] *  d['losses']) + (lose * lossav))/(d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] *  d['Entries'])/100) + totdiff)/(d['Entries'] + Ins))* 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat6(z, L,d, lock):
    buy_in = [0] * 24
    PL = 0
    Bal = 0
    Hourly_PL = [0] * 7
    PerStock = [[[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]],
                    [[], 0, ["BUY"], ["SELL"]], [[], 0, ["BUY"], ["SELL"]]]
    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = [0] * 20
    mark_up = [0] * 20
    stop_loss = [0] * 20
    Entry_Price = [0] * 20
    Recent_Exit = [1] * 20
    hourly = [0] * 24
    winwin = 0
    loslos = 0
    totdiff = 0
    avgpercent = 0
    low = [10000] * 20
    high = [0] * 20
    times_entered = [0] * 20



    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/'  + str(file_list[z])

    times_entered = [0] * 20
    Recent_Exit = [1] * 20

    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    Entry_data = []
    Price_data = []
    Symbol_data = []
    Time_data = []

    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0,22):
                    row[ii] = float(row[ii])

                Entry = row[:21]
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time)-1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue


            if (Entry[11] < 0):
                Recent_Exit[count] = 0
            PerStock[count][0] = symbol
            if (Entry[0] < 0) and (Entry[3] > 0) and (Entry[8] > price) and (Entry[16] == price) and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = 8 // Entry[9]
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1
                PerStock[count][1] = PerStock[count][1] - (numshare * price)
                stop_loss[count] = price - (Entry[9] * 1.5)
                mark_up[count] = price + (Entry[9] * 2.194)
                times_entered[count] = 0

                PerStock[count][2].append(str(hour % 12) + ':' + str("{:02d}".format(min)) + '(' + str(price) + ')')
            if Pos[count] > 0:
                if (((price > mark_up[count]) or (price < stop_loss[count])) and (Entry[15] == price)) or (hour == 14 and min == 59):
                    if ((Entry[0] < 0) and (Entry[3] > 0) and (Entry[8] > price)) and (not (hour == 14 and min == 59)):
                        stop_loss[count] = price - (Entry[9] * 1.5)
                        mark_up[count] = price + (Entry[9] * 2.194)
                    else:
                        returnval = Pos[count] * price
                        Bal = Bal + returnval
                        PerStock[count][1] = PerStock[count][1] + (Pos[count] * price)
                        PerStock[count][3].append(str(hour % 12) + ':' + str("{:02d}".format(min)) + '(' + str(price) + ')')
                        diff = price - Entry_Price[count]
                        diff = diff / Entry_Price[count]
                        totdiff = totdiff + diff
                        avgpercent = 100 * totdiff / Ins
                        if price > Entry_Price[count]:
                            win = win + 1
                            wintot = price - Entry_Price[count]
                            wintot = wintot / Entry_Price[count]
                            winwin = winwin + wintot
                            winav = 100 * winwin / win


                        else:
                            lose = lose + 1
                            losstot = Entry_Price[count] - price
                            losstot = losstot / Entry_Price[count]
                            loslos = loslos + losstot
                            lossav = 100 * loslos / lose
                        Entry_Price[count] = 0
                        Pos[count] = 0
                        Recent_Exit[count] = 1
                        buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL =  Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z*7):(z*7+7)] =  Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] *  d['wins']) + (win * winav))/(d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] *  d['losses']) + (lose * lossav))/(d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] *  d['Entries'])/100) + totdiff)/(d['Entries'] + Ins))* 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat7(z, L,d, lock):
    buy_in = ([0] * 24)
    PL = 0
    Bal = 0
    Hourly_PL = ([0] * 7)
    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = ([0] * 20)
    mark_up = ([0] * 20)
    stop_loss = ([0] * 20)
    Entry_Price = ([0] * 20)
    Recent_Exit = ([1] * 20)
    hourly = ([0] * 24)
    totdiff = 0
    avgpercent = 0
    low = ([10000] * 20)
    high = ([0] * 20)
    times_entered = ([0] * 20)
    winwin = 0
    loslos = 0
    buymin = [0] * 20
    buyhour = [0] * 20
    sellmin = [0] * 20
    sellhour = [0] *20
    avgtime = 0
    tottime = 0
    path = 'C:/Users/shiva/PycharmProjects/BotTest/v6'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/' + str(file_list[z])

    times_entered = ([0] * 20)
    Recent_Exit = ([1] * 20)

    now = datetime.now()


    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0, 22):
                    try:
                        row[ii] = float(row[ii])
                    except:
                        bbb =4
                Entry = (row[:21])
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time) - 1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue

            Enter = price > Entry[10] - (Entry[10] - Entry[9]) *.35 and Entry[14] < 30
            if Enter  and (((Entry[19] - Entry[20]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):

                numshare = int(20 // Entry[7])
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1

                stop_loss[count] = price - (Entry[7] * 6)
                mark_up[count] = price + (Entry[7] * 4)
                buymin[count] = min
                buyhour[count] = hour



                times_entered[count] = 0

            if Pos[count] > 0:
                if (price > mark_up[count]) and (times_entered[count] < 12):
                    mark_up[count] = mark_up[count] + (Entry[7] * 4)
                    stop_loss[count] = stop_loss[count] + (Entry[7] * 4)
                    numshare = math.ceil((Pos[count] // 7))
                    Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                    Bal = Bal - (numshare * price)
                    Pos[count] = Pos[count] + numshare

                    times_entered[count] = times_entered[count] + 1
                    Ins = Ins + 1
                if (price < stop_loss[count] ) or (hour == 14 and min == 59):
                # if (((price > mark_up[count]) or (price < stop_loss[count]))) or (hour == 14 and min == 59):
                # if Entry[15] < -70 or (hour == 14 and min == 59):
                    returnval = Pos[count] * price
                    Bal = Bal + returnval
                    diff = price - Entry_Price[count]
                    diff = diff / Entry_Price[count]
                    totdiff = totdiff + diff
                    avgpercent = 100 * totdiff / Ins

                    time = ((hour * 60) + min) - ((buyhour[count] * 60) + buymin[count])
                    tottime = tottime + time

                    if price > Entry_Price[count]:
                        win = win + 1
                        wintot = price - Entry_Price[count]
                        wintot = wintot / Entry_Price[count]
                        winwin = winwin + wintot
                        winav = 100 * winwin / win


                    else:
                        lose = lose + 1
                        losstot = Entry_Price[count] - price
                        losstot = losstot / Entry_Price[count]
                        loslos = loslos + losstot
                        lossav = 100 * loslos / lose

                    Entry_Price[count] = 0
                    Pos[count] = 0
                    Recent_Exit[count] = 1
                    buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL = Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z * 7):(z * 7 + 7)] = Hourly_PL
        print("read", mydate)  #
        d['Balance'] = d['Balance'] + PL
        d['tottime'] = d['tottime'] + tottime

        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] * d['wins']) + (win * winav)) / (d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] * d['losses']) + (lose * lossav)) / (d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] * d['Entries']) / 100) + totdiff) / (d['Entries'] + Ins)) * 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release

def strat8(z, L,d, lock):
    buy_in = ([0] * 30)
    PL = 0
    Bal = 0
    Hourly_PL = ([0] * 7)
    win = 0
    winav = 0
    wintot = 0
    lose = 0
    lossav = 0
    avgtime = 0
    losstot = 0
    Ins = 0
    maxspend = 0
    numPos = 0
    Pos = ([0] * 30)
    mark_up = ([0] * 30)
    flag = [0] * 30
    stop_loss = ([0] * 30)
    Entry_Price = ([0] * 30)
    Recent_Exit = ([1] * 30)
    hourly = ([0] * 30)
    condition = [0]*30
    totdiff = 0
    trigger = [0] * 30
    trigger2 = [0] * 30
    avgpercent = 0
    low = ([10000] * 30)
    high = ([0] * 30)
    shareconst = .7
    times_entered = ([0] * 30)
    winwin = 0
    loslos = 0
    buyhour = [0] * 30
    buymin = [0] * 30
    tottime = 0
    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    live = 0
    test = 0
    mydate = file_list[z]
    filename = path + '/' + str(file_list[z])

    times_entered = ([0] * 30)
    Recent_Exit = ([1] * 30)

    now = datetime.now()


    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0
    # reads replay data
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = 0
        for row in readCSV:
            if a == 0:
                a = 1
                continue
            try:
                row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL"
            except:
                pass
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            # print(counter)
            if counter == 0:
                counter = counter + 1
                count = 0
                stockval = 0
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":

                for ii in range(0, 22):
                    row[ii] = float(row[ii])

                Entry = (row[:21])
                price = row[21]
                symbol = row[22]
                time = row[23]
                time = time[1:len(time) - 1]
                t = re.split(':', time)
                hour = int(t[0])
                min = int(t[1])
                numPos = 0
            else:
                count = 0
                stockval = 0
                continue
            qualifies = 1


            strats =  [[1.96, 0.47], 0, 0, -1, 0, 1, -1, 1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 30, 49, 30, 0]
            sellstrat = strats[0]
            buystrat = strats[1:]
            for i, strat in enumerate(buystrat):
                if strat == 0:
                    continue
                if i != 8 and i != 14 and i != 17 and i != 18 and i != 19 and i != 20:
                    if (Entry[i] * strat <= 0):
                        qualifies = 0
                        break
                if i == 8 or i == 14 or i == 20:
                    if ((Entry[i] - price) * strat <= 0):
                        qualifies = 0
                        break
                if i == 17 or i == 18 or i == 19:
                    if (strat / abs(strat)) * Entry[i] < strat:
                        qualifies = 0
                        break
            if Entry[7] > 0 and Entry[6] > 0 and Entry[4] :
                trigger[count] = 1
            if trigger[count] == 1 and Entry[7] > 0 and Entry[6] > 0 and Entry[4] < 0:
                Enter = 1
                trigger[count] = 0
            else:
                Enter = 0
            if Enter and (((Entry[15] - Entry[16]) / price) < .003) and (Pos[count] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                condition[count] = 0
                Enter = 0
                buyhour[count] = hour
                buymin[count] = min
                numshare = math.ceil((10 // Entry[9])* shareconst)
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price)
                Pos[count] = numshare
                Entry_Price[count] = price
                Ins = Ins + 1

                stop_loss[count] = price - (Entry[9] * sellstrat[0])
                mark_up[count] = price + (Entry[9] * 00000)




                times_entered[count] = 0

            if Pos[count] > 0:
                # if (price < mark_up[count]) and (times_entered[count] < 12):
                #     stop_loss[count] = stop_loss[count] + (Entry[9] * sellstrat[0])
                #     # mark_up[count] = mark_up[count] + (Entry[9] * sellstrat[1])
                #
                #     numshare = math.ceil((Pos[count] // 7) * shareconst)
                #     Entry_Price[count] = (Entry_Price[count] * Pos[count] + price * numshare) / (Pos[count] + numshare)
                #     Bal = Bal - (numshare * price)
                #     Pos[count] = Pos[count] + numshare
                #
                #     times_entered[count] = times_entered[count] + 1
                #     Ins = Ins + 1
                # # if (price > mark_up[count]) or (hour == 14 and min == 59):
                if Entry[4] > 0:
                    trigger2[count] = 1
                if (Entry[5] < 0) or (Entry[4] < 1 and trigger2[count] == 1)  or (hour == 14 and min == 59):
                        trigger2[count] = 0
                        time = ((hour * 60) + min) - ((buyhour[count] * 60) + buymin[count])
                        tottime = tottime + time
                        avgtime = tottime / Ins

                        returnval = Pos[count] * price
                        Bal = Bal + returnval
                        diff = price - Entry_Price[count]
                        diff = diff / Entry_Price[count]
                        totdiff = totdiff + diff
                        avgpercent = 100 * totdiff / Ins
                        if price > Entry_Price[count]:
                            win = win + 1
                            wintot = price - Entry_Price[count]
                            wintot = wintot / Entry_Price[count]
                            winwin = winwin + wintot
                            winav = 100 * winwin / win


                        else:
                            lose = lose + 1
                            losstot = Entry_Price[count] - price
                            losstot = losstot / Entry_Price[count]
                            loslos = loslos + losstot
                            lossav = 100 * loslos / lose

                        Entry_Price[count] = 0
                        Pos[count] = 0
                        Recent_Exit[count] = 1
                        buy_in[count] = 0

            stockval = Pos[count] * price + stockval
            if Pos[count] > 0:
                numPos = numPos + 1
            if stockval > maxspend:
                maxspend = int(stockval)
            PL = Bal + stockval
            Hourly_PL[hour - 8] = int(PL)
            count = count + 1

        lock.acquire
        L[(z * 7):(z * 7 + 7)] = Hourly_PL
        print("read", mydate)  #
        d['avgtime'] = avgtime
        d['Balance'] = d['Balance'] + PL
        if (d['wins'] + win) == 0:
            d['avgwin'] = 0
        else:
            d['avgwin'] = ((d['avgwin'] * d['wins']) + (win * winav)) / (d['wins'] + win)
        if (d['losses'] + lose) == 0:
            d['avgloss'] = 0
        else:
            d['avgloss'] = ((d['avgloss'] * d['losses']) + (lose * lossav)) / (d['losses'] + lose)
        if (d['Entries'] + Ins) == 0:
            d['avgpercent'] = 0
        else:
            d['avgpercent'] = ((((d['avgpercent'] * d['Entries']) / 100) + totdiff) / (d['Entries'] + Ins)) * 100
        d['wins'] = d['wins'] + win
        d['losses'] = d['losses'] + lose
        d['Entries'] = d['Entries'] + Ins
        if d['maxspend'] < maxspend:
            d['maxspend'] = maxspend
        lock.release







if __name__ == '__main__':
    print("running")
    with Manager() as manager:
        d = manager.dict()
        d['Balance'] = 0
        d['Entries'] = 0
        d['wins'] = 0
        d['losses'] = 0
        d['avgwin'] = 0
        d['avgloss'] = 0
        d['maxspend'] = 0
        d['avgpercent'] = 0
        d['tottime'] = 0
        L = manager.list(range(num_files*7))
        lock = Lock()
        processes = []
        for i in range(0, math.ceil(num_files/threads)):
            if (i == math.ceil(num_files/threads) - 1) and (num_files%threads !=0):
                target = num_files % threads
            else:
                target = threads
            for j in range(0,target):
                p = Process(target=strat8, args = ((i * threads + j),L,d, lock))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()




        for n in range(0,len(L)):
            q = n//7
            if(q > 0):
                L[n] = L[n] + L[q * 7 -1]
        ll = ([0])
        for l in range(0,len(L)):
            # ll = np.append(ll,L[l])
            ll.append(L[l])
        straight = findstraight(ll)

        print("           ", d['Balance'], "         ", "wins:", d['wins'], "     avgwin:", round(d['avgwin'], 3), "%","     losses", d['losses'], "     avgloss:", round(d['avgloss'] , 3), "%", "     Buys:", int(d['Entries']), "  ", "  maxspend:",  d['maxspend'], "  ", d['avgpercent'], "% ","   Days", num_files, " Straightness:",straight, "         Averagehold:",(d['tottime']/d['Entries']) ," minutes")
        print('That took {} seconds'.format(time.time() - starttime))

        plt.plot(ll, label = "12.1")
        plt.annotate("12.1",xy = (7*num_files,ll[-1]))
        for n in range(0, (len(ll))//7):
           plt.axvline(x= n*7)
        plt.ylabel('some numbers')
        plt.legend(loc="upper left")
        plt.show()

