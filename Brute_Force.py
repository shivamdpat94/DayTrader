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
import numpy as np



path = 'C:/Users/shiva/PycharmProjects/BotTest'
files = os.listdir(path)
file_list =[]
for n in range(0,len(files)):
    if files[n].endswith('.csv'):
        file_list.append(files[n])



num_files = len(file_list) - 1
rettot = 0




def test(strats,results,index):
    print("START")
    time.sleep(5)
    print("END")


def findstraight( x):
    straightness = 0
    for n in range(0, len(x) - 1):
        q = math.sqrt((-1) ** 2 + (x[n] - x[n + 1]) ** 2)
        straightness = straightness + q
    straight = straightness
    p = math.sqrt((len(x)**2) + (x[-1]**2))
    straight = p/straight
    return straight


def makestrat(filters):
    def makeres():
        PL = 0
        avgpercent = 0
        Ins = 0
        Performance_Array = [0]
        maxspend = 0
        straightness = 0
        aa = [PL , avgpercent, Performance_Array, Ins, maxspend, straightness]
        return aa

    var = []
    res = []

    for sellout in range(0,7):
        if filters >= 1:
            for hk1 in range(-1, 2):
                if filters >= 2:
                    for hk5 in range(-1,2):
                        if filters >= 3:
                            for hk15 in range(-1,2):
                                if filters >= 4:
                                    for hk30 in range(-1,2):
                                        if filters >= 5:
                                            for hk1h in range(-1,2):
                                                if filters >= 6:
                                                    for MaD1 in range (-1,2):
                                                        if filters >= 7:
                                                            for hk4h in range (-1,2):
                                                                if filters >= 8:
                                                                    for hk1D in range (-1,2):
                                                                        if filters >= 9:
                                                                            for Ma1 in range(-1,2):
                                                                                if filters >= 10:
                                                                                    for hk1m in range(-1,2):
                                                                                        if filters >= 11:
                                                                                            for hk5m in range (-1,2):
                                                                                                if filters >= 12:
                                                                                                    for MaD5 in range (-1,2):
                                                                                                        if filters >= 13:
                                                                                                            for MaD15 in range (-1,2):
                                                                                                                if filters >= 14:
                                                                                                                    for Ma5 in range (-1,2):
                                                                                                                        if filters >= 15:
                                                                                                                            for RSI1 in range(0,7):
                                                                                                                                if filters >= 16:
                                                                                                                                    for RSI5 in range(0,7):
                                                                                                                                        if filters >= 17:
                                                                                                                                            for RSI15 in range(0,7):
                                                                                                                                                if filters >= 18:
                                                                                                                                                    for VWAP in range(0,3):
                                                                                                                                                        a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5,MaD15,Ma5,0,0,RSI1,RSI5,RSI15,VWAP]
                                                                                                                                                        if len(a) < 22:
                                                                                                                                                            c = 22 - len(a)
                                                                                                                                                            for d in range(0,c):
                                                                                                                                                                a.append(0)
                                                                                                                                                        aa = makeres()
                                                                                                                                                        var.append(a)
                                                                                                                                                        res.append(aa)
                                                                                                                                                else:
                                                                                                                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5,MaD15,Ma5,0,0,RSI1,RSI5,RSI15]
                                                                                                                                                    if len(a) < 22:
                                                                                                                                                        c = 22 - len(a)
                                                                                                                                                        for d in range(0,c):
                                                                                                                                                            a.append(0)
                                                                                                                                                    aa = makeres()
                                                                                                                                                    var.append(a)
                                                                                                                                                    res.append(aa)
                                                                                                                                        else:
                                                                                                                                            a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5,MaD15,Ma5,0,0,RSI1,RSI5]
                                                                                                                                            if len(a) < 22:
                                                                                                                                                c = 22 - len(a)
                                                                                                                                                for d in range(0,c):
                                                                                                                                                    a.append(0)
                                                                                                                                            aa = makeres()
                                                                                                                                            var.append(a)
                                                                                                                                            res.append(aa)
                                                                                                                                else:
                                                                                                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5,MaD15,Ma5,0,0,RSI1]
                                                                                                                                    if len(a) < 22:
                                                                                                                                        c = 22 - len(a)
                                                                                                                                        for d in range(0,c):
                                                                                                                                            a.append(0)
                                                                                                                                    aa = makeres()
                                                                                                                                    var.append(a)
                                                                                                                                    res.append(aa)
                                                                                                                        else:
                                                                                                                            a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5,MaD15,Ma5]
                                                                                                                            if len(a) < 22:
                                                                                                                                c = 22 - len(a)
                                                                                                                                for d in range(0, c):
                                                                                                                                    a.append(0)
                                                                                                                            aa = makeres()
                                                                                                                            var.append(a)
                                                                                                                            res.append(aa)
                                                                                                                else:
                                                                                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5,MaD15]
                                                                                                                    if len(a) < 22:
                                                                                                                        c = 22 - len(a)
                                                                                                                        for d in range(0,c):
                                                                                                                            a.append(0)
                                                                                                                    aa = makeres()
                                                                                                                    var.append(a)
                                                                                                                    res.append(aa)
                                                                                                        else:
                                                                                                            a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m,MaD5]
                                                                                                            if len(a) < 22:
                                                                                                                c = 22 - len(
                                                                                                                    a)
                                                                                                                for d in range(0,c):
                                                                                                                    a.append(0)
                                                                                                            aa = makeres()
                                                                                                            var.append(a)
                                                                                                            res.append(aa)
                                                                                                else:
                                                                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m,hk5m]
                                                                                                    if len(a) < 22:
                                                                                                        c = 22 - len(a)
                                                                                                        for d in range(0,
                                                                                                                       c):
                                                                                                            a.append(0)
                                                                                                    aa = makeres()
                                                                                                    var.append(a)
                                                                                                    res.append(aa)
                                                                                        else:
                                                                                            a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1,0,hk1m]
                                                                                            if len(a) < 22:
                                                                                                c = 22 - len(a)
                                                                                                for d in range(0, c):
                                                                                                    a.append(0)
                                                                                            aa = makeres()
                                                                                            var.append(a)
                                                                                            res.append(aa)
                                                                                else:
                                                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D,Ma1]
                                                                                    if len(a) < 22:
                                                                                        c = 22 - len(a)
                                                                                        for d in range(0, c):
                                                                                            a.append(0)
                                                                                    aa = makeres()
                                                                                    var.append(a)
                                                                                    res.append(aa)
                                                                        else:
                                                                            a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h,hk1D]
                                                                            if len(a) < 22:
                                                                                c = 22 - len(a)
                                                                                for d in range(0, c):
                                                                                    a.append(0)
                                                                            aa = makeres()
                                                                            var.append(a)
                                                                            res.append(aa)
                                                                else:
                                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1,hk4h]
                                                                    if len(a) < 22:
                                                                        c = 22 - len(a)
                                                                        for d in range(0, c):
                                                                            a.append(0)
                                                                    aa = makeres()
                                                                    var.append(a)
                                                                    res.append(aa)
                                                        else:
                                                            a = [sellout, hk1,hk5,hk15,hk30,hk1h,MaD1]
                                                            if len(a) < 22:
                                                                c = 22 - len(a)
                                                                for d in range(0, c):
                                                                    a.append(0)
                                                            aa = makeres()
                                                            var.append(a)
                                                            res.append(aa)
                                                else:
                                                    a = [sellout, hk1,hk5,hk15,hk30,hk1h]
                                                    if len(a) < 22:
                                                        c = 22 - len(a)
                                                        for d in range(0, c):
                                                            a.append(0)
                                                    aa = makeres()
                                                    var.append(a)
                                                    res.append(aa)
                                        else:
                                            a = [sellout, hk1,hk5,hk15,hk30]
                                            if len(a) < 22:
                                                c = 22 - len(a)
                                                for d in range(0, c):
                                                    a.append(0)
                                            aa = makeres()
                                            var.append(a)
                                            res.append(aa)
                                else:
                                    a = [sellout, hk1,hk5,hk15]
                                    if len(a) < 22:
                                        c = 22 - len(a)
                                        for d in range(0, c):
                                            a.append(0)
                                    aa = makeres()
                                    var.append(a)
                                    res.append(aa)
                        else:
                            a = [sellout, hk1,hk5]
                            if len(a) < 22:
                                c = 22 - len(a)
                                for d in range(0, c):
                                    a.append(0)
                            aa = makeres()
                            var.append(a)
                            res.append(aa)
                else:
                    a = [sellout, hk1]
                    if len(a) < 22:
                        c = 22 - len(a)
                        for d in range(0, c):
                            a.append(0)
                    aa = makeres()
                    var.append(a)
                    res.append(aa)
    return var, res



def compute( Price_Data,  Entry_Data, Time_Data, strats,results,index, day):
    import time as ttime
    buy_in = [0] * 24
    PL = 0
    Bal = results[index][0]
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
    Pos = [0] * 20
    mark_up = [0] * 20
    stop_loss = [0] * 20
    Entry_Price = [0] * 20
    Recent_Exit = [1] * 20
    hourly = [0] * 24
    totdiff = 0
    avgpercent = 0
    low = [10000] * 20
    high = [0] * 20
    times_entered = [0] * 20
    ii = len(Entry_Data[0])
    sellstrat = strats[0]

    if sellstrat == 0:
        sellcombo = [.5, .5]
    if sellstrat == 1:
        sellcombo = [.5, 1]
    if sellstrat == 2:
        sellcombo = [1, .5]
    if sellstrat == 3:
        sellcombo = [1, 1]
    if sellstrat == 4:
        sellcombo = [1, 2]
    if sellstrat == 5:
        sellcombo = [2, 1]
    if sellstrat == 6:
        sellcombo = [.5,2]
    newstrats = strats[1:]


    for q in range (0,len(Price_Data)):
        qualifies = [1] * ii
        Entry = Entry_Data[q]
        price = Price_Data[q]
        time = Time_Data[q]
        t = re.split(':', time)
        hour = int(t[0])
        min = int(t[1])
        for y in range(0,ii):
            for i, strat in enumerate (newstrats):
                    if strat == 0:
                        continue
                    if i != 8 and i != 14 and i != 17 and i != 18 and i != 19 and i != 20:
                        if (Entry[y][i] * strat <= 0):
                            qualifies[y] = 0
                            break
                    if i == 8 or i == 14 or i == 20:
                        if((Entry[y][i] - price[y]) * strat <= 0):
                            qualifies[y] = 0
                            break
                    if i == 17 or i == 18 or i == 19:
                         if (strat/abs(strat)) * Entry[y][i] < strat:
                            qualifies[y] = 0
                            break
            if (qualifies[y] == 1) and (((Entry[y][15] - Entry[y][16]) / price[y]) < .003) and (Pos[y] == 0) and (hour != 14 or min != 59) and (hour != 8 or min != 30):
                numshare = 25 // Entry[y][9]
                if numshare == 0:
                    numshare = 1
                Bal = Bal - (numshare * price[y])

                Pos[y] = numshare
                Entry_Price[y] = price[y]
                Ins = Ins + 1
                times_entered[y] = 0

                stop_loss[y] = price[y] - (Entry[y][9] * sellcombo[0])
                mark_up[y] = price[y] + (Entry[y][9] * sellcombo[1])
        for y in range(0, ii):
                 if Pos[y] > 0:
                    if (price[y] < stop_loss[y]) and (times_entered[y] < 12):
                        stop_loss[y] = stop_loss[y] - (Entry[y][9])* sellcombo[0]
                        numshare = Pos[y] // 7
                        Entry_Price[y] = (Entry_Price[y] * Pos[y] + price[y] * numshare) / (Pos[y] + numshare)
                        Bal = Bal - (numshare * price[y])
                        Pos[y] = Pos[y] + numshare
                        times_entered[y] = times_entered[y] + 1
                        Ins = Ins + 1
                    if ((price[y] > mark_up[y]) or (price[y] < stop_loss[y] and times_entered[y] >=12)) or (hour == 14 and min == 59):
                    #if (price[y] > mark_up[y]) or (price[y] < stop_loss[y]) or (hour == 14 and min == 59):
                        if qualifies[y] == 1 and (not (hour == 14 and min == 59)):
                            stop_loss[y] = price[y] - (Entry[y][9] * sellcombo[0])
                            mark_up[y] = price[y] + (Entry[y][9] * sellcombo[1])
                        else:
                            returnval = Pos[y] * price[y]
                            Bal = Bal + returnval
                            diff = price[y] - Entry_Price[y]
                            diff = diff / Entry_Price[y]
                            totdiff = totdiff + diff
                            avgpercent = 100 * totdiff / Ins
                            if price[y] > Entry_Price[y]:
                                win = win + 1
                                wintot = wintot + (Pos[y] * price[y] - Pos[y] * Entry_Price[y]) / (Entry_Price[y])
                                winav = wintot / win
                            else:
                                lose = lose + 1
                                losstot = losstot + (Pos[y] * Entry_Price[y] - Pos[y] * price[y]) / (
                                Entry_Price[y])
                                lossav = losstot / lose

                            Entry_Price[y] = 0
                            Pos[y] = 0
                            Recent_Exit[y] = 1
                            buy_in[y] = 0
        stockval = 0
        numPos = 0
        for y in range(0, ii):
            stockval = Pos[y] * price[y] + stockval
            if Pos[y] > 0:
                numPos = numPos + 1
        if stockval > maxspend:
            maxspend = int(stockval)
        PL = Bal + stockval
        Hourly_PL[hour - 8] = int(PL)
    try:
        avgpercent= ((((results[index][1] * results[index][3]) / 100) + totdiff) / (results[index][3] + Ins)) * 100
    except:
        pass
    temphour = results[index][2] + Hourly_PL
    results[index] = [PL, avgpercent, temphour, results[index][3] + Ins,max(maxspend,results[index][4]), findstraight(temphour)]
    return results
    # print("Computed Day ",day+1," Strategy ",index)
























programstart = time.time()




lock = Lock()

print("Making Strategies")
filters = 12

var, res = makestrat(filters)

print("Strategies Created")


BSlist = []
try:
    with open("Badstrat.csv") as fff:
        onetime = 1
        BSreader = csv.reader(fff, delimiter=',')
        for row in BSreader:
            if onetime == 1:
                onetime = 0
                continue
            a = []
            for bb in range(0,22):
                a.append(int(row[bb]))
            if len(a) < 22:
                c = 22 - len(a)
                for d in range(0,c):
                    a.append(0)
            BSlist.append(a)
    print(len(var))
    print(len(BSlist))
    BBS = len(BSlist)
    st = time.time()
    for i in range(0, len(BSlist)):
        if i % 1000 == 0:
            print(i, " out of ", BBS, " in ", time.time()-st, " seconds")
            st = time.time()
        try:
            popspot = var.index(BSlist[i])
            var.pop(popspot)
            res.pop(popspot)
        except:
            pass
    print(len(var))
    createnew = 0
except:
    print("NO PREVIOUS RECORD. WILL MAKE NEW ONE")
    createnew = 1
    ht = 0

for day in range (0,num_files-1):
    Entry_data = []
    Price_data = []
    Time_data = []
    with open("Badstrat.csv", 'a', newline='') as ffff:
        BSwriter = csv.writer(ffff)
        if createnew == 1 and ht == 0:
            header = ['Sell_strat', '1m_Entry', '5m_Entry', '15m_Entry', '30m_Entry', '1h_Entry', '1m_MA_DIFF','4h_Entry', '1D_Entry', '1M_MA_15', 'ATR', '1m_1_Bar_Ago', '5m_1_Bar_Ago', '5m_MA_DIFF','15m_MA_DIFF', '5m_MA_15', 'ASK', 'BID', 'RSI1M', 'RSI5M', 'RSI15M', 'VWAP', ' ', 'PL','AveragePercent', 'Buys', 'Maxspend','Straightness', 'Day']
            BSwriter.writerow(header)
            ht = 1

################################################################################################################################################################################################################


        if day >= 5:
            scrap = []
            for k in range (0,len(results)):
                factor = 22000/results[k][4]
                if (results[k][0]) * factor < 70 * day:
                    scrap.append(k)
                    BSwriter.writerow(strats[k] + [' '] + results[k][:2] + results[k][3:] + [day])

            pops = 0
            for l in range(0,len(scrap)):
                results.pop(scrap[l] - pops)
                strats.pop(scrap[l] - pops)

                pops = pops + 1
        # IF AFTER DAY 4, Straightness isn't met, scrap
        if day >= 4:
            scrap = []
            for k in range (0,len(results)):
                straight = findstraight(results[k][2])
                if  straight < .2:
                    scrap.append(k)
                    BSwriter.writerow(strats[k] + [' '] + results[k][:2] + results[k][3:] + [day])
            pops = 0
            for l in range(0,len(scrap)):
                results.pop(scrap[l] - pops)
                strats.pop(scrap[l] - pops)
                pops = pops + 1

        # IF BY DAY 2 NO BUYS OCURRED, SCRAP
        if day == 2:
            scrap = []
            for k in range (0,len(results)):
                if results[k][0] == 0:
                    scrap.append(k)
                    BSwriter.writerow(strats[k] + [' '] + results[k][:2] + results[k][3:] + [day])

            pops = 0
            for l in range(0,len(scrap)):
                results.pop(scrap[l] - pops)
                strats.pop(scrap[l] - pops)
                pops = pops + 1
        # IF PL DROPS BELOW -150 ON DAY 1, scrap
        if day == 1:
            scrap = []
            for k in range (0,len(results)):
                if results[k][0] < -150:
                    scrap.append(k)
                    BSwriter.writerow(strats[k] + [' '] + results[k][:2] + results[k][3:] + [day])

            pops = 0
            for l in range(0,len(scrap)):
                results.pop(scrap[l] - pops)
                strats.pop(scrap[l] - pops)
                pops = pops + 1

        if day > 1 and len(strats) == 0:
            print("NO STRATEGIES REMAINING")
            break


################################################################################################################################################################################################################



    sellrow = 0
    counter = 0
    shift = 0
    i = 0
    j = 0

    path = 'C:/Users/shiva/PycharmProjects/BotTest'
    filename = path + '/'  + str(file_list[day])

    print("Reading Day ",day + 1," of ",len(file_list)-1)
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        aaa = 0
        for row in readCSV:
            if aaa == 0:
                aaa = 1
                continue
            if row[0] != "N" and row[0] != "NULL" and row[0] != "S" and row[0] != "SELL":
                i = i + 1
                j = len(row) - 3
            else:
                break


    with open(filename) as csvfile:
        rc = sum(1 for row in csvfile)
        rrc = rc - 1
        blocks = int(rrc/(i+1))
    count = 0







    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        p = []
        a = []
        t = []
        counter = 0
        for row in readCSV:
            if counter == 0:
                counter = counter + 1
                continue
            counter = counter + 1
            if sellrow == 0 and (row[0] == "S" or row[0] == "SELL"):
                sellrow = counter + 1

            if row[0] != "N" and row[0] != "S" and row[0] != "SELL" and row[0] != "NULL":
                try:
                    p.append(float(row[j]))
                except:
                    pass
                t.append(row[j + 1])
                b = []
                for n in range(0, j):
                    try:
                        b.append(float(row[n]))
                    except:
                        b.append(row[n])
                try:
                    a.append(b)
                except:
                    pass
            else:
                Price_data.append(p)
                Entry_data.append(a)

                try:
                    Time_data.append(row[1])
                except:
                    print("AA")
                p = []
                a = []
                t = []







    print("Read Day ",day+1, " of ", len(file_list)-1)
    starttime = time.time()
    lock = Lock()
    processes = []

    if day == 0:
        strats = var
        results = res
    if len(strats) % 55 == 0:
        imax = int(len(strats)/55)
    else:
        imax = int(len(strats)/ 55) + 1


    for i in range(0, imax):
        starttime55 = time.time()
        if i == imax - 1:
            target = len(strats) % 55
        else:
            target = 55
        for j in range(0,target):
            # p = Process(target=compute, args = (Price_data,Entry_data,Time_data,strats[i*55+j],results,i * 55 + j,day,lock))
            results = compute(Price_data,Entry_data,Time_data,strats[i*55+j],results,i * 55 + j,day)
            # print((i*55+j)/len(strats))
            # p = Process(target=test, args = (0,0 ,0))
            # p.start()
            # processes.append(p)
        # for p in processes:
        #     p.join()
        print("Completed ",i*55 + 55," out of ", len(strats)," in ", time.time() - starttime55, " seconds")
    print()
    for n in range(0,len(strats)):
        print(strats[n])
        print(results[n][:2] + results[n][3:])
    print('That took {} seconds'.format(time.time() - starttime))










GSlist = []
try:
    with open("Goodstrat.csv") as fff:
        GSreader = csv.reader(fff, delimiter=',')
        first = 1
        for row in GSreader:
            if first == 1:
                first = 0
                continue
            a = []
            for b in range(0,22):
                a.append(int(row[b]))
            if len(a) < 22:
                c = 22 - len(a)
                for d in range(0,c):
                    a.append(0)
            GSlist.append(a)
    for i in range(0, len(GSlist)):
        try:
            popspot = strats.index(GSlist[i])
            strats.pop(popspot)
            results.pop(popspot)

        except:
            pass
    createnew = 0
except:
    createnew = 1
    print("NO PREVIOUS RECORD. WILL MAKE NEW ONE")








with open("Goodstrat.csv",'a',newline='') as gs:
    GSwriter = csv.writer(gs)
    if createnew == 1:
        header = ['Sell_strat','1m_Entry', '5m_Entry', '15m_Entry', '30m_Entry', '1h_Entry', '1m_MA_DIFF', '4h_Entry', '1D_Entry', '1M_MA_15', 'ATR', '1m_1_Bar_Ago', '5m_1_Bar_Ago', '5m_MA_DIFF', '15m_MA_DIFF', '5m_MA_15', 'ASK','BID', 'RSI1M', 'RSI5M','RSI15M','VWAP',' ', 'PL', 'AveragePercent', 'Buys', 'Maxspend','Straightness','Day']

        GSwriter.writerow(header)
    for i in range(0,len(results)):
        print(results[i][:2] + results[i][3:])
        print(strats[i])
        GSwriter.writerow(strats[i] + [' '] + results[i][:2] + results[i][3:] + [day])









print('Entire program took {} seconds'.format(time.time() - programstart))































